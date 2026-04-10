import logging
import os
import time

from .services1 import (
    TrimService,
    AssemblyService,
    PredictService,
    ReportService,
    FolderVerificationService,
)

logger = logging.getLogger(__name__)


class PipelineConfig:
    """Configuration for a single pipeline run."""

    def __init__(self, genus="Unknown", species="unknown", sample_name="sample",
                 genome_size="5m", proteins_file=None):
        self.genus = genus
        self.species = species
        self.sample_name = sample_name
        self.genome_size = genome_size
        self.proteins_file = proteins_file


class Pipa:
    """Orchestrator for the microbial genomic analysis pipeline."""

    STAGES = ["trimming", "assembly", "prediction", "report"]

    def __init__(self, data_dir=None):
        self.data_dir = data_dir or os.environ.get("PIPA_DATA_DIR", "./data")

    def init_app(self, app):
        self.data_dir = app.config.get("PIPA_DATA_DIR", self.data_dir)
        app.pipa = self

    def ensure_directories(self):
        svc = FolderVerificationService(self.data_dir)
        svc.run()

    def run_pipeline(self, config, status_callback=None):
        """Run the full pipeline. Returns a dict with results and timing info.

        Args:
            config: PipelineConfig with genus, species, etc.
            status_callback: Optional callable(stage, message) for progress updates.
        """
        self.ensure_directories()
        results = {"stages": {}, "errors": []}

        def _cb(msg):
            if status_callback:
                status_callback(current_stage, msg)

        stages = [
            ("trimming", self._run_trimming),
            ("assembly", lambda cb: self._run_assembly(config, cb)),
            ("prediction", lambda cb: self._run_prediction(config, cb)),
            ("report", self._run_report),
        ]

        for stage_name, stage_fn in stages:
            current_stage = stage_name
            if status_callback:
                status_callback(stage_name, f"Starting {stage_name}")
            start = time.time()
            try:
                stage_result = stage_fn(_cb)
                elapsed = time.time() - start
                results["stages"][stage_name] = {
                    "status": "completed",
                    "elapsed_seconds": round(elapsed, 1),
                    "result": stage_result,
                }
                logger.info("Stage %s completed in %.1fs", stage_name, elapsed)
            except Exception as e:
                elapsed = time.time() - start
                error_msg = str(e)
                results["stages"][stage_name] = {
                    "status": "failed",
                    "elapsed_seconds": round(elapsed, 1),
                    "error": error_msg,
                }
                results["errors"].append({"stage": stage_name, "error": error_msg})
                logger.error("Stage %s failed after %.1fs: %s", stage_name, elapsed, error_msg)
                # Continue to next stage rather than aborting entirely

        return results

    def _run_trimming(self, callback):
        svc = TrimService(self.data_dir)
        return svc.run(callback=callback)

    def _run_assembly(self, config, callback):
        svc = AssemblyService(
            self.data_dir,
            sample_name=config.sample_name,
            genome_size=config.genome_size,
        )
        return svc.run(callback=callback)

    def _run_prediction(self, config, callback):
        svc = PredictService(
            self.data_dir,
            genus=config.genus,
            species=config.species,
            proteins_file=config.proteins_file,
        )
        return svc.run(callback=callback)

    def _run_report(self, callback):
        svc = ReportService(self.data_dir)
        return svc.run(callback=callback)


pipa = Pipa()


def init_app(app):
    pipa.init_app(app)
