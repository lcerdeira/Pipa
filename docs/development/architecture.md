# Architecture

## Overview

PIPA follows a client-server architecture:

```
[Web UI (Vue.js/Quasar)] <--HTTP/JSON--> [Flask API] <--subprocess--> [Bioinformatics Tools]
```

## Backend

The Flask backend orchestrates the pipeline:

- **`app.py`** - Flask application factory, CORS, blueprint registration
- **`blueprints/api.py`** - REST API with async job execution via threading
- **`extensions/services.py`** - `Pipa` orchestrator class and `PipelineConfig`
- **`extensions/services1/`** - Individual service classes per stage

### Job Lifecycle

1. `POST /api/upload` - Files saved to `data/jobs/<job_id>/input/`
2. `POST /api/run` - Pipeline starts in a background thread
3. `GET /api/status/<job_id>` - Frontend polls for progress
4. `GET /api/results/<job_id>` - Results fetched when complete

### Pipeline Execution

For `input_type: "assembly"`, uploaded files are moved to `assembly/uploaded/` and trimming/assembly stages are skipped.

Each tool is wrapped in `_run_cmd()` which:
- Checks if the tool exists on PATH (`shutil.which`)
- Runs via `subprocess.run` with timeout and capture
- Logs stdout/stderr and raises on non-zero exit

## Frontend

Vue.js 2 + Quasar v1 SPA:

- **`Software.vue`** - Two workflow modes (reads vs annotation), tool selection
- **`Results.vue`** - Progress polling, results table, file browser
- **Vuex store** - `pipa/` module with job state, pipeline status, API actions
- **Axios** - HTTP client configured to `http://127.0.0.1:5000/api`

## Data Flow

```
User selects files + tools
    |
[uploadFiles action] --> POST /api/upload --> saves files
    |
[startPipeline action] --> POST /api/run --> background thread
    |
[pollStatus action] <-- GET /api/status (every 3s)
    |
[fetchResults action] <-- GET /api/results --> display in table
```
