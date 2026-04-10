import logging
import os
import shutil
import subprocess

logger = logging.getLogger(__name__)


class AssemblyService:
    """Handles genome assembly for Illumina (SPAdes) and Nanopore (Canu, Flye, Unicycler) data."""

    def __init__(self, data_dir, sample_name="sample", genome_size="5m"):
        self.data_dir = data_dir
        self.sample_name = sample_name
        self.genome_size = genome_size

    def _run_cmd(self, command, description):
        tool = command[0]
        if not shutil.which(tool):
            raise FileNotFoundError(f"{tool} not found in PATH. Is it installed?")
        logger.info("Running %s: %s", description, " ".join(command))
        result = subprocess.run(command, capture_output=True, text=True, timeout=36000)
        if result.returncode != 0:
            logger.error("%s failed (exit %d): %s", description, result.returncode, result.stderr)
            raise RuntimeError(f"{description} failed: {result.stderr[:500]}")
        logger.info("%s completed successfully", description)
        return result

    def run(self, callback=None):
        """Run assembly on all available trimmed data."""
        assemblies = []

        illumina_dir = os.path.join(self.data_dir, "trimmed", "illumina")
        nanopore_dir = os.path.join(self.data_dir, "trimmed", "nanopore")

        # Illumina assembly with SPAdes
        if os.path.isdir(illumina_dir) and os.listdir(illumina_dir):
            files = sorted(os.listdir(illumina_dir))
            spades_out = os.path.join(self.data_dir, "assembly", "spades")
            has_paired = any("R1" in f or "_1" in f or "val_1" in f for f in files)

            if has_paired:
                if callback:
                    callback("Assembling Illumina paired-end reads with SPAdes")
                for i in range(0, len(files) - 1, 2):
                    r1 = os.path.join(illumina_dir, files[i])
                    r2 = os.path.join(illumina_dir, files[i + 1])
                    command = [
                        "spades.py", "-1", r1, "-2", r2,
                        "--isolate", "--cov-cutoff", "auto",
                        "-o", spades_out,
                    ]
                    self._run_cmd(command, f"SPAdes paired ({files[i]}, {files[i+1]})")
                    assemblies.append(spades_out)
            else:
                if callback:
                    callback("Assembling Illumina single-end reads with SPAdes")
                for f in files:
                    fastq = os.path.join(illumina_dir, f)
                    command = [
                        "spades.py", "-s", fastq,
                        "-o", spades_out,
                    ]
                    self._run_cmd(command, f"SPAdes single ({f})")
                    assemblies.append(spades_out)

        # Nanopore assembly with Canu, Flye, Unicycler
        if os.path.isdir(nanopore_dir) and os.listdir(nanopore_dir):
            files = sorted(os.listdir(nanopore_dir))

            for f in files:
                filepath = os.path.join(nanopore_dir, f)

                # Canu
                if callback:
                    callback(f"Assembling Nanopore reads with Canu ({f})")
                canu_out = os.path.join(self.data_dir, "assembly", "canu")
                command = [
                    "canu", "-p", self.sample_name, "-d", canu_out,
                    f"genomeSize={self.genome_size}",
                    "-nanopore", filepath,
                ]
                self._run_cmd(command, f"Canu ({f})")
                assemblies.append(canu_out)

                # Flye
                if callback:
                    callback(f"Assembling Nanopore reads with Flye ({f})")
                flye_out = os.path.join(self.data_dir, "assembly", "flye")
                command = [
                    "flye", "--nano-raw", filepath,
                    "-o", flye_out,
                ]
                self._run_cmd(command, f"Flye ({f})")
                assemblies.append(flye_out)

                # Unicycler
                if callback:
                    callback(f"Assembling Nanopore reads with Unicycler ({f})")
                unicycler_out = os.path.join(self.data_dir, "assembly", "unicycler")
                command = [
                    "unicycler", "-l", filepath,
                    "-o", unicycler_out,
                ]
                self._run_cmd(command, f"Unicycler ({f})")
                assemblies.append(unicycler_out)

        return assemblies
