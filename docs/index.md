<div style="text-align: center;">
  <img src="assets/PipaLogo.jpeg" alt="PIPA Logo" width="300"/>
</div>

# PIPA - Pipeline for Microbial Genomic Analysis

PIPA is an integrated platform for microbial genomic analysis that supports Illumina, Nanopore, and PacBio sequencing data. It provides a web interface with a Flask backend that orchestrates bioinformatics tools for read trimming, genome assembly, gene prediction, and reporting.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19521044.svg)](https://doi.org/10.5281/zenodo.19521044)
[![GitHub](https://img.shields.io/github/stars/lcerdeira/Pipa?style=social)](https://github.com/lcerdeira/Pipa)

## Pipeline Overview

```
Raw Reads (FASTQ)                    Assembled Genome (FASTA)
       |                                       |
  [Trimming]                                   |
  Trim Galore / Porechop_ABI                   |
       |                                       |
  [Assembly]                                   |
  SPAdes / Canu / Flye / Unicycler             |
       |                                       |
       +---------------------------------------+
       |
  [Annotation]  <-- 47 tools in 5 categories:
  General: Prokka, Bakta, MLST, Barrnap,
           tRNAscan-SE, EggNOG, KOFAM
  Quality: BUSCO, CheckM, QUAST
  Resistance: Abricate, AMRFinderPlus, mcroni
  Mobile: PlasmidFinder, MOB-suite, Phigaro,
          PhiSpy, CRISPRCasFinder, DefenseFinder
  Typing: 27 organism-specific tools
       |
  [Report]
  KEGG-decoder
```

## Two Workflows

### Annotation Only
Upload an assembled genome (FASTA) and select which annotation tools to run. Ideal when you already have an assembly and want to quickly annotate it.

### Full Pipeline
Upload raw sequencing reads (FASTQ) from Illumina, Nanopore, or PacBio. PIPA will trim, assemble, and annotate automatically.

## Features

- **47 bioinformatics tools** organized in 5 categories
- **Generic organism support** - works with any bacterial genome
- **27 organism-specific typing tools** - auto-enabled based on genus/species
- **Selectable tools** - choose exactly which annotation tools to run
- **Desktop application** - native apps for macOS, Windows, Linux with Docker auto-setup
- **Async pipeline** - submit jobs and monitor progress in real-time
- **REST API** - programmatic access to all pipeline functionality
- **Docker support** - all tools pre-installed in [`lcerdeira/pipa`](https://hub.docker.com/r/lcerdeira/pipa) image

## Quick Start

### Desktop App (recommended)

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
2. Download PIPA from [GitHub Releases](https://github.com/lcerdeira/Pipa/releases)
3. Launch — backend starts automatically

### Docker (standalone)

```bash
docker run -d --name pipa -p 5000:5000 -v pipa-data:/data lcerdeira/pipa:latest
# API available at http://localhost:5000
```

### Conda

```bash
conda env create -f environment.yml
conda activate pipa
cd back-end && flask run --host 0.0.0.0 --port 5000
```

See [Installation](getting-started/installation.md) for detailed instructions.
