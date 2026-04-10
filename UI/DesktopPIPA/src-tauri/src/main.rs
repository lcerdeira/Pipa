// Prevents additional console window on Windows in release
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::process::{Child, Command};
use std::sync::Mutex;
use tauri::Manager;

struct FlaskProcess(Mutex<Option<Child>>);

fn find_backend_dir() -> String {
    let cwd = std::env::current_dir().unwrap_or_default();

    // Try paths relative to current working directory
    // CWD in dev is src-tauri/, so ../../../back-end = Pipa/back-end
    for relative in &["../../../back-end", "../../back-end", "../back-end", "back-end"] {
        let path = cwd.join(relative);
        if path.join("app.py").exists() {
            return path.canonicalize()
                .unwrap_or(path)
                .to_string_lossy()
                .to_string();
        }
    }

    // Try relative to executable
    if let Ok(exe_path) = std::env::current_exe() {
        if let Some(exe_dir) = exe_path.parent() {
            for relative in &["back-end", "../Resources/back-end", "../../back-end"] {
                let path = exe_dir.join(relative);
                if path.join("app.py").exists() {
                    return path.canonicalize()
                        .unwrap_or(path)
                        .to_string_lossy()
                        .to_string();
                }
            }
        }
    }

    eprintln!("[PIPA] Warning: Could not find back-end directory, tried from: {}", cwd.display());
    cwd.join("../../back-end").to_string_lossy().to_string()
}

fn find_python() -> String {
    // Check common python locations
    let candidates = if cfg!(target_os = "windows") {
        vec!["python", "python3"]
    } else {
        vec![
            "python3",
            "/opt/homebrew/Caskroom/mambaforge/base/envs/pipa/bin/python3",
            "/opt/homebrew/bin/python3",
            "/usr/local/bin/python3",
            "/usr/bin/python3",
        ]
    };

    for candidate in &candidates {
        if let Ok(output) = Command::new(candidate).arg("--version").output() {
            if output.status.success() {
                println!("[PIPA] Found Python: {}", candidate);
                return candidate.to_string();
            }
        }
    }

    "python3".to_string()
}

fn start_flask() -> Option<Child> {
    let backend_dir = find_backend_dir();
    let python = find_python();
    println!("[PIPA] Starting Flask backend from: {}", backend_dir);
    println!("[PIPA] Using Python: {}", python);

    let data_dir = dirs::data_dir()
        .unwrap_or_else(|| std::path::PathBuf::from("."))
        .join("pipa");

    // Ensure data directory exists
    let _ = std::fs::create_dir_all(&data_dir);

    match Command::new(&python)
        .args(["-m", "flask", "run", "--host", "0.0.0.0", "--port", "5000"])
        .current_dir(&backend_dir)
        .env("FLASK_APP", "app.py")
        .env("PIPA_DATA_DIR", data_dir.to_string_lossy().to_string())
        .spawn()
    {
        Ok(child) => {
            println!("[PIPA] Flask backend started (PID: {})", child.id());
            Some(child)
        }
        Err(e) => {
            eprintln!("[PIPA] Failed to start Flask backend: {}", e);
            eprintln!("[PIPA] Make sure Python 3 and Flask are installed.");
            eprintln!("[PIPA] You can also start Flask manually: cd {} && {} -m flask run --host 0.0.0.0 --port 5000", backend_dir, python);
            None
        }
    }
}

fn main() {
    tauri::Builder::default()
        .setup(|app| {
            let flask_child = start_flask();
            app.manage(FlaskProcess(Mutex::new(flask_child)));

            // Give Flask a moment to start
            let window = app.get_window("main").unwrap();
            std::thread::spawn(move || {
                std::thread::sleep(std::time::Duration::from_secs(2));
                let _ = window.eval("window.location.reload()");
            });

            Ok(())
        })
        .on_window_event(|event| {
            if let tauri::WindowEvent::Destroyed = event.event() {
                let app = event.window().app_handle();
                if let Some(flask) = app.try_state::<FlaskProcess>() {
                    if let Ok(mut guard) = flask.0.lock() {
                        if let Some(ref mut child) = *guard {
                            println!("[PIPA] Stopping Flask backend");
                            let _ = child.kill();
                        }
                    }
                }
            }
        })
        .run(tauri::generate_context!())
        .expect("error while running PIPA");
}
