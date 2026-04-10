"""Tests for the PIPA REST API."""
import io
import json
import os
import sys
import tempfile

import pytest

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app import create_app


@pytest.fixture
def app():
    """Create application for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        os.environ["PIPA_DATA_DIR"] = tmpdir
        application = create_app()
        application.config["TESTING"] = True
        # Clear shared job store between tests
        from blueprints.api import _jobs
        _jobs.clear()
        yield application


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


class TestUpload:
    def test_upload_no_files(self, client):
        response = client.post("/api/upload")
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data

    def test_upload_illumina_files(self, client):
        data = {
            "illumina": (io.BytesIO(b"@SEQ\nACGT\n+\nIIII\n"), "test_R1.fastq"),
        }
        response = client.post(
            "/api/upload",
            data=data,
            content_type="multipart/form-data",
        )
        assert response.status_code == 201
        result = json.loads(response.data)
        assert "job_id" in result
        assert "illumina" in result["uploaded"]

    def test_upload_paired_end_odd_files(self, client):
        data = {
            "illumina": (io.BytesIO(b"@SEQ\nACGT\n+\nIIII\n"), "test_R1.fastq"),
            "illumina_type": "paired",
        }
        response = client.post(
            "/api/upload",
            data=data,
            content_type="multipart/form-data",
        )
        assert response.status_code == 400


class TestRun:
    def test_run_invalid_job(self, client):
        response = client.post(
            "/api/run",
            data=json.dumps({"job_id": "nonexistent"}),
            content_type="application/json",
        )
        assert response.status_code == 400

    def test_run_missing_job_id(self, client):
        response = client.post(
            "/api/run",
            data=json.dumps({}),
            content_type="application/json",
        )
        assert response.status_code == 400


class TestStatus:
    def test_status_not_found(self, client):
        response = client.get("/api/status/nonexistent")
        assert response.status_code == 404

    def test_status_after_upload(self, client):
        # Upload first
        data = {
            "illumina": (io.BytesIO(b"@SEQ\nACGT\n+\nIIII\n"), "test.fastq"),
        }
        upload_response = client.post(
            "/api/upload",
            data=data,
            content_type="multipart/form-data",
        )
        job_id = json.loads(upload_response.data)["job_id"]

        # Check status
        response = client.get(f"/api/status/{job_id}")
        assert response.status_code == 200
        result = json.loads(response.data)
        assert result["status"] == "uploaded"


class TestResults:
    def test_results_not_found(self, client):
        response = client.get("/api/results/nonexistent")
        assert response.status_code == 404

    def test_results_before_completion(self, client):
        # Upload first
        data = {
            "illumina": (io.BytesIO(b"@SEQ\nACGT\n+\nIIII\n"), "test.fastq"),
        }
        upload_response = client.post(
            "/api/upload",
            data=data,
            content_type="multipart/form-data",
        )
        job_id = json.loads(upload_response.data)["job_id"]

        # Try to get results before running
        response = client.get(f"/api/results/{job_id}")
        assert response.status_code == 409


class TestJobs:
    def test_list_empty_jobs(self, client):
        response = client.get("/api/jobs")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["jobs"] == []

    def test_list_jobs_after_upload(self, client):
        # Upload
        data = {
            "illumina": (io.BytesIO(b"@SEQ\nACGT\n+\nIIII\n"), "test.fastq"),
        }
        client.post("/api/upload", data=data, content_type="multipart/form-data")

        response = client.get("/api/jobs")
        assert response.status_code == 200
        result = json.loads(response.data)
        assert len(result["jobs"]) == 1
