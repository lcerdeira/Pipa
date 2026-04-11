![PIPA_Logo](/assets/PipaLogo.jpeg)
# PIPA - Pipeline for Microbial Genomic Analysis

![Code Count](https://img.shields.io/github/languages/count/lcerdeira/pipa)
![Main Code Base](https://img.shields.io/github/languages/top/lcerdeira/pipa)
![Version](https://img.shields.io/badge/version-2.0-red)
![License](https://img.shields.io/badge/license-GPLv3-blue)
![Last Commit](https://img.shields.io/github/last-commit/lcerdeira/pipa)
[![Documentation](https://readthedocs.org/projects/pipa-tool/badge/?version=latest)](https://pipa-tool.readthedocs.io/en/latest/)

PIPA is an integrated platform for microbial genomic analysis that supports Illumina, Nanopore, and PacBio sequencing data. It provides a web interface and desktop application with a Flask backend that orchestrates bioinformatics tools for read trimming, genome assembly, gene prediction, and reporting.

**[Full Documentation](https://pipa-tool.readthedocs.io/en/latest/)** | **[GitHub Repository](https://github.com/lcerdeira/Pipa)** | **[Download Desktop App](https://github.com/lcerdeira/Pipa/releases)**

## Pipeline Stages

| Stage | Tools | Description |
|-------|-------|-------------|
| **Trimming** | Trim Galore, Porechop | Quality trimming of Illumina and Nanopore reads |
| **Assembly** | SPAdes, Canu, Flye, Unicycler | Genome assembly from short and long reads |
| **Prediction** | Prokka, MLST, Barrnap, Abricate, AMRFinderPlus, Kleborate*, Phigaro, KOFAM | Gene annotation, typing, resistance, and phage detection |
| **Report** | KEGG-decoder | Functional pathway visualization |

*\*Kleborate runs only when genus is Klebsiella*

## Desktop Application

Download native installers from the [Releases](https://github.com/lcerdeira/Pipa/releases) page:

| Platform | File | Architecture |
|----------|------|--------------|
| **macOS (Apple Silicon)** | `PIPA_2.0.0_aarch64.dmg` | M1, M2, M3, M4 |
| **macOS (Intel)** | `PIPA_2.0.0_x64.dmg` | Intel Macs |
| **Windows** | `PIPA_2.0.0_x64-setup.exe` | 64-bit Windows 10/11 |
| **Linux (Debian/Ubuntu)** | `pipa_2.0.0_amd64.deb` | Debian-based |
| **Linux (Universal)** | `pipa_2.0.0_amd64.AppImage` | Any 64-bit Linux |

## Quick Start (Docker)

```bash
# Clone the repository
git clone https://github.com/lcerdeira/Pipa.git
cd Pipa

# Start the backend with all bioinformatics tools
docker-compose up -d

# The API is now available at http://localhost:5000
# See examples/run_example.sh for a usage walkthrough
```

## Quick Start (Web SPA)

```bash
# Install backend dependencies
cd back-end
pip install -r requirements.txt
flask run --host 0.0.0.0 --port 5000

# In another terminal, install and run the frontend
cd UI/DesktopPIPA
yarn install
npx quasar dev
```

Open http://localhost:8080 in your browser.

## Installation (Conda)

For native installation with all bioinformatics tools:

```bash
# Create the conda environment
conda env create -f environment.yml
conda activate pipa

# Start the backend
cd back-end
flask run --host 0.0.0.0 --port 5000
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/upload` | Upload sequencing files (multipart form) |
| `POST` | `/api/run` | Start pipeline with configuration |
| `GET` | `/api/status/<job_id>` | Get pipeline progress and status |
| `GET` | `/api/results/<job_id>` | Get pipeline results |
| `GET` | `/api/results/<job_id>/files/<path>` | Download result file |
| `GET` | `/api/jobs` | List all jobs |

### Example API Usage

```bash
# Upload files
curl -X POST http://localhost:5000/api/upload \
  -F "illumina=@reads_R1.fastq.gz" \
  -F "illumina=@reads_R2.fastq.gz" \
  -F "illumina_type=paired"

# Start pipeline
curl -X POST http://localhost:5000/api/run \
  -H "Content-Type: application/json" \
  -d '{"job_id": "abc123", "genus": "Klebsiella", "species": "pneumoniae", "genome_size": "5.5m"}'

# Check status
curl http://localhost:5000/api/status/abc123
```

## Configuration

The pipeline accepts these parameters per run:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `genus` | Unknown | Organism genus (used by Prokka, Kleborate) |
| `species` | unknown | Organism species |
| `sample_name` | sample | Name for the analysis run |
| `genome_size` | 5m | Estimated genome size (used by Canu) |
| `input_type` | reads | `reads` (full pipeline) or `assembly` (annotation only) |
| `tools` | [] | Annotation tools to run (e.g., `["prokka", "mlst", "abricate"]`) |

Environment variable `PIPA_DATA_DIR` controls where data is stored (default: `./data`).

## Project Structure

```
Pipa/
  back-end/              # Flask REST API
    app.py               # Application entry point
    blueprints/          # API and view routes
    extensions/          # Pipeline services
      services.py        # Pipeline orchestrator
      services1/         # Individual service modules
    tests/               # API tests
  UI/DesktopPIPA/        # Desktop & web application
    src/                 # Vue.js components and store
    src-tauri/           # Tauri desktop wrapper (Rust)
  docs/                  # Documentation (MkDocs)
  environment.yml        # Conda environment specification
  Dockerfile             # Container build
  docker-compose.yml     # Container orchestration
  examples/              # Example scripts
```

## Running Tests

```bash
cd back-end
pip install pytest
python -m pytest tests/ -v
```

## Contact

Dr Louise Cerdeira - Louise.Cerdeira@gmail.com

## License

Copyright 2021-2026 Louise Cerdeira. GPL-3.0.

## Citation

If you use PIPA in your research, please cite:

> Cerdeira, L. PIPA: Pipeline for Microbial Genomic Analysis. https://github.com/lcerdeira/Pipa
