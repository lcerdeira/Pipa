import logging
import os
import threading
import time
import uuid

from flask import Blueprint, current_app, jsonify, request, send_from_directory
from werkzeug.utils import secure_filename

from extensions.services import PipelineConfig

logger = logging.getLogger(__name__)

api_bp = Blueprint("api", __name__)

# In-memory job store (single-user desktop app, no need for DB)
_jobs = {}


def _get_job(job_id):
    job = _jobs.get(job_id)
    if not job:
        return None
    return job


@api_bp.route("/upload", methods=["POST"])
def upload_files():
    """Upload sequencing files. Expects multipart form data with platform-keyed files.

    Form fields:
        illumina_type: "paired" or "single" (default: "single")
        illumina: file(s)
        nanopore: file(s)
        pacbio: file(s)
    """
    data_dir = current_app.config["PIPA_DATA_DIR"]
    job_id = str(uuid.uuid4())[:8]
    job_data_dir = os.path.join(data_dir, "jobs", job_id)

    uploaded = {}

    for platform in ["illumina", "nanopore", "pacbio"]:
        files = request.files.getlist(platform)
        if not files or files[0].filename == "":
            continue

        platform_dir = os.path.join(job_data_dir, "input", platform)
        os.makedirs(platform_dir, exist_ok=True)

        saved = []
        for f in files:
            filename = secure_filename(f.filename)
            filepath = os.path.join(platform_dir, filename)
            f.save(filepath)
            saved.append(filename)
            logger.info("Saved %s to %s", filename, platform_dir)

        uploaded[platform] = saved

    if not uploaded:
        return jsonify({"error": "No files uploaded"}), 400

    illumina_type = request.form.get("illumina_type", "single")
    if illumina_type == "paired" and "illumina" in uploaded:
        if len(uploaded["illumina"]) % 2 != 0:
            return jsonify({"error": "Paired-end requires an even number of files"}), 400

    _jobs[job_id] = {
        "id": job_id,
        "data_dir": job_data_dir,
        "uploaded": uploaded,
        "status": "uploaded",
        "stage": None,
        "message": "Files uploaded, ready to run",
        "progress": 0,
        "results": None,
        "errors": [],
        "created_at": time.time(),
    }

    return jsonify({"job_id": job_id, "uploaded": uploaded}), 201


@api_bp.route("/run", methods=["POST"])
def run_pipeline():
    """Start a pipeline run.

    JSON body:
        job_id: str (from upload)
        genus: str (default: "Unknown")
        species: str (default: "unknown")
        sample_name: str (default: "sample")
        genome_size: str (default: "5m")
    """
    data = request.get_json(silent=True) or {}
    job_id = data.get("job_id")

    if not job_id or job_id not in _jobs:
        return jsonify({"error": "Invalid or missing job_id"}), 400

    job = _jobs[job_id]
    if job["status"] == "running":
        return jsonify({"error": "Pipeline is already running"}), 409

    config = PipelineConfig(
        genus=data.get("genus", "Unknown"),
        species=data.get("species", "unknown"),
        sample_name=data.get("sample_name", "sample"),
        genome_size=data.get("genome_size", "5m"),
        proteins_file=data.get("proteins_file"),
    )

    job["status"] = "running"
    job["stage"] = "initializing"
    job["progress"] = 0

    # Run pipeline in background thread
    def _run():
        pipa = current_app.pipa
        total_stages = len(pipa.STAGES)
        completed = 0

        def status_callback(stage, message):
            nonlocal completed
            stage_idx = pipa.STAGES.index(stage) if stage in pipa.STAGES else completed
            job["stage"] = stage
            job["message"] = message
            job["progress"] = int((stage_idx / total_stages) * 100)

        try:
            # Override data_dir for this job
            original_data_dir = pipa.data_dir
            pipa.data_dir = job["data_dir"]
            pipa.ensure_directories()

            results = pipa.run_pipeline(config, status_callback=status_callback)

            pipa.data_dir = original_data_dir

            job["results"] = results
            job["status"] = "completed" if not results["errors"] else "completed_with_errors"
            job["progress"] = 100
            job["message"] = "Pipeline completed"
            job["stage"] = "done"
        except Exception as e:
            logger.exception("Pipeline failed for job %s", job_id)
            job["status"] = "failed"
            job["message"] = str(e)
            job["errors"].append(str(e))

    # Need app context in thread
    app = current_app._get_current_object()

    def _run_with_context():
        with app.app_context():
            _run()

    thread = threading.Thread(target=_run_with_context, daemon=True)
    thread.start()

    return jsonify({"job_id": job_id, "status": "running"}), 202


@api_bp.route("/status/<job_id>")
def get_status(job_id):
    """Get pipeline status for a job."""
    job = _get_job(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404

    return jsonify({
        "job_id": job["id"],
        "status": job["status"],
        "stage": job["stage"],
        "message": job["message"],
        "progress": job["progress"],
        "errors": job["errors"],
    })


@api_bp.route("/results/<job_id>")
def get_results(job_id):
    """Get pipeline results for a completed job."""
    job = _get_job(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404

    if job["status"] not in ("completed", "completed_with_errors"):
        return jsonify({
            "error": "Pipeline not yet completed",
            "status": job["status"],
        }), 409

    # Collect all result files
    result_files = []
    job_data_dir = job["data_dir"]
    for dirpath, dirnames, filenames in os.walk(job_data_dir):
        for f in filenames:
            full_path = os.path.join(dirpath, f)
            rel_path = os.path.relpath(full_path, job_data_dir)
            result_files.append(rel_path)

    return jsonify({
        "job_id": job["id"],
        "status": job["status"],
        "results": job["results"],
        "files": result_files,
    })


@api_bp.route("/results/<job_id>/files/<path:filename>")
def download_file(job_id, filename):
    """Download a specific result file."""
    job = _get_job(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404

    return send_from_directory(job["data_dir"], filename, as_attachment=True)


@api_bp.route("/jobs")
def list_jobs():
    """List all jobs."""
    jobs = []
    for job in _jobs.values():
        jobs.append({
            "job_id": job["id"],
            "status": job["status"],
            "stage": job["stage"],
            "progress": job["progress"],
            "created_at": job["created_at"],
        })
    return jsonify({"jobs": jobs})
