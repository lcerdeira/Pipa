# Quick Start

## Annotate an Assembled Genome

This is the fastest way to use PIPA — upload an assembled genome and run annotation tools.

### Via Web UI

1. Open `http://localhost:8080`
2. Click **Start** to go to the Software page
3. Select **Annotation Only** workflow
4. Upload your FASTA file (`.fasta`, `.fa`, or `.fna`)
5. Select annotation tools (Prokka, MLST, Barrnap, Abricate are on by default)
6. Set the genus and species of your organism
7. Click **Submit**
8. Monitor progress on the Results page

### Via API

```bash
# Upload a FASTA file
curl -X POST http://localhost:5000/api/upload \
  -F "illumina=@my_assembly.fasta"

# Start annotation (replace JOB_ID with the returned job_id)
curl -X POST http://localhost:5000/api/run \
  -H "Content-Type: application/json" \
  -d '{
    "job_id": "JOB_ID",
    "genus": "Escherichia",
    "species": "coli",
    "input_type": "assembly",
    "tools": ["prokka", "mlst", "barrnap", "abricate"]
  }'

# Check status
curl http://localhost:5000/api/status/JOB_ID

# Get results when complete
curl http://localhost:5000/api/results/JOB_ID
```

## Run the Full Pipeline

For raw sequencing reads (FASTQ), PIPA runs trimming, assembly, then annotation.

### Via Web UI

1. Select **Full Pipeline (Raw Reads)** workflow
2. Check **Illumina**, **Nanopore**, or **PacBio**
3. Upload your FASTQ files (paired-end or single-end)
4. Set genome size (for Nanopore/PacBio assembly)
5. Click **Submit**

### Via API

```bash
# Upload paired-end Illumina reads
curl -X POST http://localhost:5000/api/upload \
  -F "illumina=@reads_R1.fastq.gz" \
  -F "illumina=@reads_R2.fastq.gz" \
  -F "illumina_type=paired"

# Start full pipeline
curl -X POST http://localhost:5000/api/run \
  -H "Content-Type: application/json" \
  -d '{
    "job_id": "JOB_ID",
    "genus": "Klebsiella",
    "species": "pneumoniae",
    "input_type": "reads",
    "genome_size": "5.5m"
  }'
```

## Example with Test Data

```bash
bash examples/run_example.sh
```
