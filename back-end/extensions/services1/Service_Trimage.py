import logging
import os
import shutil
import subprocess

logger = logging.getLogger(__name__)


class TrimService:
    """Handles read trimming for Illumina (Trim Galore) and Nanopore (Porechop) data."""

    def __init__(self, data_dir):
        self.data_dir = data_dir

    def _run_cmd(self, command, description):
        tool = command[0]
        if not shutil.which(tool):
            raise FileNotFoundError(f"{tool} not found in PATH. Is it installed?")
        logger.info("Running %s: %s", description, " ".join(command))
        result = subprocess.run(command, capture_output=True, text=True, timeout=7200)
        if result.returncode != 0:
            logger.error("%s failed (exit %d): %s", description, result.returncode, result.stderr)
            raise RuntimeError(f"{description} failed: {result.stderr[:500]}")
        logger.info("%s completed successfully", description)
        return result

    def run(self, callback=None):
        """Run trimming on all available input data. callback(msg) for progress updates."""
        trimmed = []

        illumina_dir = os.path.join(self.data_dir, "input", "illumina")
        nanopore_dir = os.path.join(self.data_dir, "input", "nanopore")
        illumina_out = os.path.join(self.data_dir, "trimmed", "illumina")
        nanopore_out = os.path.join(self.data_dir, "trimmed", "nanopore")

        # Illumina trimming with Trim Galore
        if os.path.isdir(illumina_dir) and os.listdir(illumina_dir):
            files = sorted(os.listdir(illumina_dir))
            has_paired = any("R1" in f or "_1" in f for f in files)

            if has_paired:
                if callback:
                    callback("Trimming Illumina paired-end reads with Trim Galore")
                for i in range(0, len(files) - 1, 2):
                    r1 = os.path.join(illumina_dir, files[i])
                    r2 = os.path.join(illumina_dir, files[i + 1])
                    command = [
                        "trim_galore", "--paired", "--no_report_file",
                        "-o", illumina_out, r1, r2,
                    ]
                    self._run_cmd(command, f"Trim Galore paired ({files[i]}, {files[i+1]})")
                    trimmed.extend([r1, r2])
            else:
                if callback:
                    callback("Trimming Illumina single-end reads with Trim Galore")
                for f in files:
                    fastq = os.path.join(illumina_dir, f)
                    command = [
                        "trim_galore", "--no_report_file",
                        "-o", illumina_out, fastq,
                    ]
                    self._run_cmd(command, f"Trim Galore single ({f})")
                    trimmed.append(fastq)

        # Nanopore trimming with Porechop
        if os.path.isdir(nanopore_dir) and os.listdir(nanopore_dir):
            if callback:
                callback("Trimming Nanopore reads with Porechop")
            output_file = os.path.join(nanopore_out, "output_reads.fastq.gz")
            command = ["porechop_abi", "-i", nanopore_dir, "-o", output_file]
            self._run_cmd(command, "Porechop")
            trimmed.append(output_file)

        return trimmed
