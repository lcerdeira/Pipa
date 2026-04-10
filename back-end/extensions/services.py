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
                 genome_size="5m", proteins_file=None, input_type="reads", tools=None):
        self.genus = genus
        self.species = species
        self.sample_name = sample_name
        self.genome_size = genome_size
        self.proteins_file = proteins_file
        self.input_type = input_type  # "reads" or "assembly"
        self.tools = tools or []  # list of tool keys to run


class Pipa:
    """Orchestrator for the microbial genomic analysis pipeline."""

    STAGES = ["trimming", "assembly", "prediction", "report"]

    def __init__(self, data_dir=None):
        self.data_dir = data_dir or os.environ.get("PIPA_DATA_DIR", "./data")

    def init_app(self, app):
        self.data_dir = app.config.get("PIPA_DATA_DIR", self.data_dir)
        app.pipa = self

    def run_pipeline(self, config, data_dir=None, status_callback=None):
        """Run the full pipeline. Returns a dict with results and timing info.

        Args:
            config: PipelineConfig with genus, species, etc.
            data_dir: Job-specific data directory. Falls back to self.data_dir.
            status_callback: Optional callable(stage, message) for progress updates.
        """
        dd = data_dir or self.data_dir

        # Ensure directory structure
        FolderVerificationService(dd).run()

        results = {"stages": {}, "errors": []}

        def _cb(msg):
            if status_callback:
                status_callback(current_stage, msg)

        stages = []

        if config.input_type == "reads":
            stages.append(("trimming", lambda cb: TrimService(dd).run(callback=cb)))
            stages.append(("assembly", lambda cb: AssemblyService(
                dd, sample_name=config.sample_name, genome_size=config.genome_size
            ).run(callback=cb)))

        stages.append(("prediction", lambda cb: PredictService(
            dd, genus=config.genus, species=config.species,
            proteins_file=config.proteins_file, tools=config.tools
        ).run(callback=cb)))
        stages.append(("report", lambda cb: ReportService(dd).run(callback=cb)))

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

        return results


pipa = Pipa()


def init_app(app):
    pipa.init_app(app)
