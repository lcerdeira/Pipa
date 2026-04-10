# Full Pipeline Workflow

The Full Pipeline processes raw sequencing reads through trimming, assembly, annotation, and reporting.

## Stages

### 1. Trimming

| Platform | Tool | Description |
|----------|------|-------------|
| Illumina | Trim Galore | Quality and adapter trimming (wraps Cutadapt) |
| Nanopore | Porechop | Adapter removal for Oxford Nanopore reads |

### 2. Assembly

| Platform | Tool | Description |
|----------|------|-------------|
| Illumina | SPAdes | De Bruijn graph assembler with careful mode |
| Nanopore | Canu | Overlap-layout-consensus assembler for long reads |
| Nanopore | Flye | Fast long-read assembler using repeat graphs |
| Nanopore | Unicycler | Hybrid assembler (can use both short and long reads) |

### 3. Annotation

All annotation tools from the [Annotation Workflow](annotation.md) are available.

### 4. Report

KEGG-decoder generates metabolic pathway visualizations from Prokka output.

## Input Requirements

### Illumina

- FASTQ files (`.fastq` or `.fastq.gz`)
- Single-end: one file per sample
- Paired-end: two files per sample (R1 and R2), must be uploaded together

### Nanopore

- FASTQ files from MinION, GridION, or PromethION
- Basecalled reads (not raw FAST5)

### PacBio

- FASTQ or BAM files from Sequel/Sequel II

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| Genome Size | For Nanopore | Estimated genome size (e.g., `5m` for 5 Mbp) used by Canu |
| Genus | Yes | Organism genus |
| Species | Yes | Organism species |
| Sample Name | Yes | Name for the analysis run |
