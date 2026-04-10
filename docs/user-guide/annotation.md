# Annotation Workflow

The Annotation workflow allows you to run selected annotation tools on an assembled genome (FASTA) without performing trimming or assembly.

## Input

- A FASTA file containing assembled contigs or a complete genome
- Accepted extensions: `.fasta`, `.fa`, `.fna`

## Available Tools

Select any combination of the following tools:

| Tool | Description | Default |
|------|-------------|---------|
| **Prokka** | Rapid prokaryotic gene annotation (CDS, rRNA, tRNA, tmRNA) | On |
| **MLST** | Multi-locus sequence typing against PubMLST databases | On |
| **Barrnap** | Ribosomal RNA gene prediction (5S, 16S, 23S) | On |
| **Abricate** | Antimicrobial resistance gene screening against multiple databases | On |
| **AMRFinderPlus** | NCBI's AMR gene and point mutation detection | Off |
| **PlasmidFinder** | Plasmid replicon identification | Off |
| **MOB-suite** | Plasmid classification and typing | Off |
| **CRISPRCasFinder** | CRISPR array and Cas gene detection | Off |
| **tRNAscan-SE** | Transfer RNA gene prediction | Off |
| **Phigaro** | Prophage region detection | Off |
| **Kleborate** | Klebsiella-specific virulence and resistance typing (only for Klebsiella) | Off |
| **KOFAM** | KEGG Orthology functional annotation | Off |

## Output Files

Each tool produces output in the job's `predicted/` directory:

- **Prokka**: `.gff` (annotations), `.gbk` (GenBank), `.faa` (proteins), `.ffn` (genes), `.txt` (summary)
- **MLST**: `.tsv` with sequence type and allele profile
- **Barrnap**: `.gff` with rRNA gene locations
- **Abricate**: `.tsv` with resistance gene hits, coverage, and identity
- **AMRFinderPlus**: `.tsv` with AMR genes and point mutations

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| Genus | Yes | Organism genus (used by Prokka for annotation) |
| Species | Yes | Organism species |
| Sample Name | Yes | Name for the analysis run |

!!! tip
    You can type a custom genus or species if yours isn't in the dropdown list.

!!! note
    Kleborate only runs when the genus is set to "Klebsiella".
