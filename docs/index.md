<div style="text-align: center;">
  <img src="assets/PipaLogo.jpeg" alt="PIPA Logo" width="300"/>
</div>

# PIPA - Pipeline for Microbial Genomic Analysis

PIPA is an integrated platform for microbial genomic analysis that supports Illumina, Nanopore, and PacBio sequencing data. It provides a web interface with a Flask backend that orchestrates bioinformatics tools for read trimming, genome assembly, gene prediction, and reporting.

## Pipeline Overview

```
Raw Reads (FASTQ)                    Assembled Genome (FASTA)
       |                                       |
  [Trimming]                                   |
  Trim Galore / Porechop                       |
       |                                       |
  [Assembly]                                   |
  SPAdes / Canu / Flye / Unicycler             |
       |                                       |
       +---------------------------------------+
       |
  [Annotation]  <-- Choose your tools:
  Prokka, MLST, Barrnap, Abricate,
  AMRFinderPlus, PlasmidFinder, MOB-suite,
  CRISPRCasFinder, tRNAscan-SE, Phigaro,
  Kleborate, KOFAM
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

- **Generic organism support** - works with any bacterial genome, not limited to a specific species
- **Selectable tools** - choose exactly which annotation tools to run
- **Async pipeline** - submit jobs and monitor progress in real-time
- **REST API** - programmatic access to all pipeline functionality
- **Docker support** - reproducible deployment with all tools pre-installed

## Quick Start

```bash
# Docker (recommended)
docker-compose up -d
# Open http://localhost:8080

# Or local install
conda env create -f environment.yml
conda activate pipa
cd back-end && flask run --host 0.0.0.0 --port 5000
```

See [Installation](getting-started/installation.md) for detailed instructions.
