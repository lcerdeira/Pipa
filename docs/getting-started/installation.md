# Installation

PIPA can be installed using Docker (recommended) or via Conda for local development.

## Docker (Recommended)

```bash
git clone https://github.com/lcerdeira/Pipa.git
cd Pipa
docker-compose up -d
```

The API will be available at `http://localhost:5000` and the web UI at `http://localhost:8080`.

## Conda / Mamba

### 1. Create the environment

```bash
conda env create -f environment.yml
conda activate pipa
```

This installs Python, Flask, and all bioinformatics tools (Prokka, SPAdes, MLST, etc.) via Bioconda.

### 2. Start the backend

```bash
cd back-end
pip install -r requirements.txt
flask run --host 0.0.0.0 --port 5000
```

### 3. Start the frontend

```bash
cd UI/DesktopPIPA
yarn install
npx quasar dev
```

The web UI will be available at `http://localhost:8080`.

## System Requirements

- **OS**: Linux or macOS (Docker works on all platforms)
- **RAM**: 8 GB minimum, 16 GB recommended for assembly
- **Disk**: 10 GB for tools + space for your data
- **Python**: 3.9+
- **Node.js**: 16+ (for frontend development)

## Verifying the Installation

```bash
# Check the API
curl http://localhost:5000/api/jobs

# Expected response:
# {"jobs": []}
```
