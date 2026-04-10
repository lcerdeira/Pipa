import logging
import os
import shutil
import subprocess

logger = logging.getLogger(__name__)


class ReportService:
    """Generates pipeline reports from prediction outputs."""

    def __init__(self, data_dir):
        self.data_dir = data_dir

    def _run_cmd(self, command, description):
        tool = command[0]
        if not shutil.which(tool):
            logger.warning("%s not found in PATH, skipping %s", tool, description)
            return None
        logger.info("Running %s: %s", description, " ".join(command))
        result = subprocess.run(command, capture_output=True, text=True, timeout=3600)
        if result.returncode != 0:
            logger.error("%s failed (exit %d): %s", description, result.returncode, result.stderr)
            raise RuntimeError(f"{description} failed: {result.stderr[:500]}")
        logger.info("%s completed successfully", description)
        return result

    def run(self, callback=None):
        """Generate reports from Prokka output using KEGG-decoder."""
        prokka_dir = os.path.join(self.data_dir, "predicted", "prokka")
        report_dir = os.path.join(self.data_dir, "reports")
        os.makedirs(report_dir, exist_ok=True)

        reports = []

        if not os.path.isdir(prokka_dir):
            logger.warning("No Prokka output found, skipping report generation")
            return reports

        # Find .txt files in Prokka output (could be in subdirectories per assembler)
        for root, dirs, files in os.walk(prokka_dir):
            for f in files:
                if f.endswith(".txt"):
                    text_file = os.path.join(root, f)
                    name = os.path.splitext(f)[0]

                    if callback:
                        callback(f"Generating KEGG-decoder report for {name}")

                    report_tsv = os.path.join(report_dir, f"{name}.tsv")
                    report_svg = os.path.join(report_dir, f"{name}.svg")

                    command = [
                        "KEGG-decoder",
                        "--input", text_file,
                        "--output", report_tsv,
                        "--vizoption", "static",
                    ]
                    result = self._run_cmd(command, f"KEGG-decoder ({name})")
                    if result:
                        reports.append({
                            "name": name,
                            "tsv": report_tsv,
                            "svg": report_svg,
                        })

        return reports
