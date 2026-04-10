# API Reference

PIPA provides a REST API on port 5000 for programmatic access.

## Endpoints

### Upload Files

```
POST /api/upload
```

Upload sequencing files. Accepts multipart form data.

**Form fields:**

| Field | Type | Description |
|-------|------|-------------|
| `illumina` | file(s) | Illumina FASTQ or FASTA files |
| `nanopore` | file(s) | Nanopore FASTQ files |
| `pacbio` | file(s) | PacBio FASTQ files |
| `illumina_type` | string | `"paired"` or `"single"` (default: `"single"`) |

**Response** (201):
```json
{
  "job_id": "abc12345",
  "uploaded": {
    "illumina": ["reads_R1.fastq.gz", "reads_R2.fastq.gz"]
  }
}
```

---

### Start Pipeline

```
POST /api/run
```

Start a pipeline run for a previously uploaded job.

**JSON body:**

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `job_id` | string | required | Job ID from upload |
| `genus` | string | `"Unknown"` | Organism genus |
| `species` | string | `"unknown"` | Organism species |
| `sample_name` | string | `"sample"` | Analysis name |
| `genome_size` | string | `"5m"` | Estimated genome size (for Canu) |
| `input_type` | string | `"reads"` | `"reads"` or `"assembly"` |
| `tools` | array | `[]` | Tool keys to run (e.g., `["prokka", "mlst"]`) |

**Response** (202):
```json
{
  "job_id": "abc12345",
  "status": "running"
}
```

---

### Get Status

```
GET /api/status/<job_id>
```

**Response** (200):
```json
{
  "job_id": "abc12345",
  "status": "running",
  "stage": "prediction",
  "message": "Running Prokka on direct assembly",
  "progress": 50,
  "errors": []
}
```

Status values: `uploaded`, `running`, `completed`, `completed_with_errors`, `failed`

---

### Get Results

```
GET /api/results/<job_id>
```

Returns results and list of output files for a completed job.

**Response** (200):
```json
{
  "job_id": "abc12345",
  "status": "completed",
  "results": {
    "stages": {
      "prediction": {
        "status": "completed",
        "elapsed_seconds": 237.7,
        "result": {"mlst_direct": "ecoli\tST10\t..."}
      }
    },
    "errors": []
  },
  "files": [
    "predicted/prokka/direct/direct.gff",
    "predicted/mlst/direct_mlst.tsv"
  ]
}
```

---

### Download File

```
GET /api/results/<job_id>/files/<path>
```

Download a specific result file.

---

### List Jobs

```
GET /api/jobs
```

Returns all jobs with their current status.
