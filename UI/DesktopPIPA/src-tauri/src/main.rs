// Prevents additional console window on Windows in release
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::process::{Child, Command, Stdio};
use std::sync::Mutex;
use std::io::{BufRead, BufReader};
use tauri::Manager;

const DOCKER_IMAGE: &str = "lcerdeira/pipa:latest";
const CONTAINER_NAME: &str = "pipa-backend";
const BACKEND_PORT: u16 = 5000;

struct BackendProcess(Mutex<BackendState>);

enum BackendState {
    Docker(String),    // container ID
    Flask(Child),      // local Flask process
    None,
}

// ── Docker helpers ────────────────────────────────────────────────────────

fn is_docker_available() -> bool {
    Command::new("docker")
        .args(["info"])
        .stdout(Stdio::null())
        .stderr(Stdio::null())
        .status()
        .map(|s| s.success())
        .unwrap_or(false)
}

fn is_image_present() -> bool {
    Command::new("docker")
        .args(["image", "inspect", DOCKER_IMAGE])
        .stdout(Stdio::null())
        .stderr(Stdio::null())
        .status()
        .map(|s| s.success())
        .unwrap_or(false)
}

fn stop_existing_container() {
    let _ = Command::new("docker")
        .args(["rm", "-f", CONTAINER_NAME])
        .stdout(Stdio::null())
        .stderr(Stdio::null())
        .status();
}

fn pull_image(window: &tauri::Window) -> bool {
    println!("[PIPA] Pulling Docker image: {}", DOCKER_IMAGE);
    let _ = window.emit("backend-status", "pulling");

    let child = Command::new("docker")
        .args(["pull", DOCKER_IMAGE])
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn();

    match child {
        Ok(mut proc) => {
            // Stream pull progress to the frontend
            if let Some(stderr) = proc.stderr.take() {
                let reader = BufReader::new(stderr);
                for line in reader.lines().flatten() {
                    println!("[PIPA] docker pull: {}", line);
                    let _ = window.emit("pull-progress", &line);
                }
            }
            proc.wait().map(|s| s.success()).unwrap_or(false)
        }
        Err(e) => {
            eprintln!("[PIPA] Failed to pull image: {}", e);
            false
        }
    }
}

fn start_container() -> Option<String> {
    let data_dir = dirs::data_dir()
        .unwrap_or_else(|| std::path::PathBuf::from("."))
        .join("pipa");
    let _ = std::fs::create_dir_all(&data_dir);

    stop_existing_container();

    let output = Command::new("docker")
        .args([
            "run", "-d",
            "--name", CONTAINER_NAME,
            "-p", &format!("{}:{}", BACKEND_PORT, BACKEND_PORT),
            "-v", &format!("{}:/data", data_dir.to_string_lossy()),
            DOCKER_IMAGE,
        ])
        .output();

    match output {
        Ok(out) if out.status.success() => {
            let container_id = String::from_utf8_lossy(&out.stdout).trim().to_string();
            println!("[PIPA] Docker container started: {}", &container_id[..12.min(container_id.len())]);
            Some(container_id)
        }
        Ok(out) => {
            eprintln!("[PIPA] Failed to start container: {}", String::from_utf8_lossy(&out.stderr));
            None
        }
        Err(e) => {
            eprintln!("[PIPA] Failed to run docker: {}", e);
            None
        }
    }
}

fn stop_container() {
    println!("[PIPA] Stopping Docker container");
    let _ = Command::new("docker")
        .args(["stop", CONTAINER_NAME])
        .stdout(Stdio::null())
        .stderr(Stdio::null())
        .status();
    let _ = Command::new("docker")
        .args(["rm", CONTAINER_NAME])
        .stdout(Stdio::null())
        .stderr(Stdio::null())
        .status();
}

// ── Local Flask fallback ──────────────────────────────────────────────────

fn find_backend_dir() -> Option<String> {
    let cwd = std::env::current_dir().unwrap_or_default();

    for relative in &["../../../back-end", "../../back-end", "../back-end", "back-end"] {
        let path = cwd.join(relative);
        if path.join("app.py").exists() {
            return Some(path.canonicalize().unwrap_or(path).to_string_lossy().to_string());
        }
    }

    if let Ok(exe_path) = std::env::current_exe() {
        if let Some(exe_dir) = exe_path.parent() {
            for relative in &["back-end", "../Resources/back-end", "../../back-end"] {
                let path = exe_dir.join(relative);
                if path.join("app.py").exists() {
                    return Some(path.canonicalize().unwrap_or(path).to_string_lossy().to_string());
                }
            }
        }
    }

    None
}

fn find_python() -> Option<String> {
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
                return Some(candidate.to_string());
            }
        }
    }
    None
}

fn start_flask() -> Option<Child> {
    let backend_dir = find_backend_dir()?;
    let python = find_python()?;
    println!("[PIPA] Starting local Flask from: {}", backend_dir);

    let data_dir = dirs::data_dir()
        .unwrap_or_else(|| std::path::PathBuf::from("."))
        .join("pipa");
    let _ = std::fs::create_dir_all(&data_dir);

    Command::new(&python)
        .args(["-m", "flask", "run", "--host", "0.0.0.0", "--port", &BACKEND_PORT.to_string()])
        .current_dir(&backend_dir)
        .env("FLASK_APP", "app.py")
        .env("PIPA_DATA_DIR", data_dir.to_string_lossy().to_string())
        .spawn()
        .ok()
}

// ── Tauri commands (callable from JS) ─────────────────────────────────────

#[tauri::command]
fn get_backend_mode(state: tauri::State<BackendProcess>) -> String {
    match *state.0.lock().unwrap() {
        BackendState::Docker(_) => "docker".to_string(),
        BackendState::Flask(_) => "local".to_string(),
        BackendState::None => "none".to_string(),
    }
}

#[tauri::command]
fn is_docker_installed() -> bool {
    is_docker_available()
}

// ── Wait for backend to respond ───────────────────────────────────────────

fn wait_for_backend(timeout_secs: u64) -> bool {
    let start = std::time::Instant::now();
    let url = format!("http://127.0.0.1:{}/api/jobs", BACKEND_PORT);

    while start.elapsed().as_secs() < timeout_secs {
        if let Ok(output) = Command::new("curl")
            .args(["-s", "-o", "/dev/null", "-w", "%{http_code}", &url])
            .output()
        {
            let code = String::from_utf8_lossy(&output.stdout);
            if code.trim() == "200" {
                println!("[PIPA] Backend is ready!");
                return true;
            }
        }
        std::thread::sleep(std::time::Duration::from_millis(500));
    }
    false
}

// ── Main ──────────────────────────────────────────────────────────────────

fn main() {
    tauri::Builder::default()
        .setup(|app| {
            let window = app.get_window("main").unwrap();
            let window_clone = window.clone();

            // Start backend in a background thread
            let backend_state = std::thread::spawn(move || -> BackendState {
                // Strategy: Try Docker first, fall back to local Flask
                if is_docker_available() {
                    let _ = window_clone.emit("backend-status", "checking-docker");
                    println!("[PIPA] Docker is available");

                    // Pull image if not present
                    if !is_image_present() {
                        let _ = window_clone.emit("backend-status", "pulling");
                        if !pull_image(&window_clone) {
                            eprintln!("[PIPA] Failed to pull image, trying local Flask");
                            let _ = window_clone.emit("backend-status", "pull-failed");
                        }
                    }

                    // Start container
                    if is_image_present() {
                        let _ = window_clone.emit("backend-status", "starting-docker");
                        if let Some(id) = start_container() {
                            let _ = window_clone.emit("backend-status", "waiting");
                            if wait_for_backend(30) {
                                let _ = window_clone.emit("backend-status", "ready");
                                return BackendState::Docker(id);
                            } else {
                                eprintln!("[PIPA] Docker container started but backend not responding");
                                stop_container();
                            }
                        }
                    }
                } else {
                    println!("[PIPA] Docker not available");
                }

                // Fallback: local Flask
                let _ = window_clone.emit("backend-status", "starting-local");
                println!("[PIPA] Falling back to local Flask");
                if let Some(child) = start_flask() {
                    let _ = window_clone.emit("backend-status", "waiting");
                    if wait_for_backend(10) {
                        let _ = window_clone.emit("backend-status", "ready");
                        return BackendState::Flask(child);
                    }
                }

                let _ = window_clone.emit("backend-status", "failed");
                eprintln!("[PIPA] No backend available. Install Docker Desktop or Python + Flask.");
                BackendState::None
            }).join().unwrap_or(BackendState::None);

            app.manage(BackendProcess(Mutex::new(backend_state)));
            Ok(())
        })
        .invoke_handler(tauri::generate_handler![get_backend_mode, is_docker_installed])
        .on_window_event(|event| {
            if let tauri::WindowEvent::Destroyed = event.event() {
                let app = event.window().app_handle();
                if let Some(state) = app.try_state::<BackendProcess>() {
                    if let Ok(mut guard) = state.0.lock() {
                        match &mut *guard {
                            BackendState::Docker(_) => {
                                stop_container();
                            }
                            BackendState::Flask(ref mut child) => {
                                println!("[PIPA] Stopping Flask backend");
                                let _ = child.kill();
                            }
                            BackendState::None => {}
                        }
                    }
                }
            }
        })
        .run(tauri::generate_context!())
        .expect("error while running PIPA");
}
