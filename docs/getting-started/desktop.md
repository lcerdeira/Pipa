# Desktop Application

PIPA provides native desktop installers for Windows, Linux, and macOS. The desktop app wraps the web interface in a native window and automatically starts the Flask backend when launched.

## Download

Download the latest installer for your platform from the [GitHub Releases](https://github.com/lcerdeira/Pipa/releases) page.

| Platform | File | Architecture |
|----------|------|--------------|
| **macOS (Apple Silicon)** | `PIPA_x.x.x_aarch64.dmg` | M1, M2, M3, M4 |
| **macOS (Intel)** | `PIPA_x.x.x_x64.dmg` | Intel Macs |
| **Windows** | `PIPA_x.x.x_x64-setup.exe` or `PIPA_x.x.x_x64_en-US.msi` | 64-bit Windows 10/11 |
| **Linux (Debian/Ubuntu)** | `pipa_x.x.x_amd64.deb` | 64-bit Debian-based |
| **Linux (Universal)** | `pipa_x.x.x_amd64.AppImage` | Any 64-bit Linux |

## Installation

### macOS

1. Download the `.dmg` file for your Mac (Apple Silicon or Intel)
2. Open the `.dmg` file
3. Drag **PIPA** to the **Applications** folder
4. On first launch, right-click the app and select **Open** (macOS Gatekeeper may block unsigned apps)

!!! note "macOS Security"
    If macOS shows "PIPA can't be opened because it is from an unidentified developer", go to **System Preferences > Security & Privacy > General** and click **Open Anyway**.

### Windows

1. Download the `.exe` installer or `.msi` package
2. Run the installer and follow the setup wizard
3. PIPA will be available in the Start Menu

!!! note "Windows Defender"
    Windows SmartScreen may warn about an unrecognized app. Click **More info** > **Run anyway**.

### Linux

**Debian/Ubuntu (.deb):**

```bash
sudo dpkg -i pipa_2.0.0_amd64.deb
sudo apt-get install -f  # install any missing dependencies
```

**Any Linux (.AppImage):**

```bash
chmod +x pipa_2.0.0_amd64.AppImage
./pipa_2.0.0_amd64.AppImage
```

## Prerequisites

The desktop app provides the graphical interface, but the bioinformatics tools must be installed separately. You have two options:

### Option A: Conda Environment (Recommended)

Install all tools via Conda/Mamba:

```bash
# Download the environment file from the PIPA repository
curl -O https://raw.githubusercontent.com/lcerdeira/Pipa/main/environment.yml

# Create the environment
conda env create -f environment.yml
conda activate pipa
```

Then launch PIPA desktop — it will detect the tools on your PATH.

### Option B: Docker Backend

Run the backend with all tools in Docker, and use the desktop app as the frontend:

```bash
# Start the backend with all bioinformatics tools
docker-compose up -d

# Then open the PIPA desktop app — it connects to localhost:5000
```

### Option C: Individual Tool Installation

Install tools manually using your system package manager:

**Ubuntu/Debian:**
```bash
sudo apt-get install prokka mlst barrnap
pip install abricate
```

**macOS (Homebrew + Bioconda):**
```bash
brew install brewsci/bio/prokka
conda install -c bioconda mlst barrnap abricate spades flye
```

## Troubleshooting

### "Flask backend failed to start"

The desktop app tries to start Flask automatically. If it fails:

1. Make sure Python 3 is installed and on your PATH
2. Install Flask: `pip install flask flask-cors`
3. Or start Flask manually:
   ```bash
   cd /path/to/Pipa/back-end
   pip install -r requirements.txt
   flask run --host 0.0.0.0 --port 5000
   ```
4. Then open the PIPA desktop app

### "Connection refused" or blank screen

The app connects to `http://127.0.0.1:5000`. Make sure:

- Flask is running on port 5000
- No firewall is blocking localhost connections
- Try opening `http://127.0.0.1:5000/api/jobs` in your browser to verify

### macOS: "App is damaged and can't be opened"

Run this in Terminal:
```bash
xattr -cr /Applications/PIPA.app
```

### Linux: AppImage won't start

Make sure FUSE is installed:
```bash
sudo apt-get install fuse libfuse2
```

## Building from Source

If you want to build the desktop app yourself:

```bash
# Prerequisites: Node.js 18+, Rust, Cargo
cd UI/DesktopPIPA

# Install dependencies
yarn install

# Build the web SPA
npx quasar build

# Build the Tauri desktop app
npx @tauri-apps/cli build
```

The installer will be in `src-tauri/target/release/bundle/`.
