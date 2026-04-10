import logging
import os
import shutil
import subprocess

logger = logging.getLogger(__name__)


class PredictService:
    """Handles gene prediction and annotation (Prokka, MLST, Barrnap, Abricate, etc.)."""

    def __init__(self, data_dir, genus="Unknown", species="unknown",
                 proteins_file=None):
        self.data_dir = data_dir
        self.genus = genus
        self.species = species
        self.proteins_file = proteins_file

    def _run_cmd(self, command, description):
        tool = command[0]
        if not shutil.which(tool):
            logger.warning("%s not found in PATH, skipping %s", tool, description)
            return None
        logger.info("Running %s: %s", description, " ".join(command))
        result = subprocess.run(command, capture_output=True, text=True, timeout=7200)
        if result.returncode != 0:
            logger.error("%s failed (exit %d): %s", description, result.returncode, result.stderr)
            raise RuntimeError(f"{description} failed: {result.stderr[:500]}")
        logger.info("%s completed successfully", description)
        return result

    def _find_assembly_fastas(self):
        """Find all .fasta files across assembly output directories."""
        assembly_dir = os.path.join(self.data_dir, "assembly")
        fastas = []
        if not os.path.isdir(assembly_dir):
            return fastas
        for folder in os.listdir(assembly_dir):
            folder_path = os.path.join(assembly_dir, folder)
            if not os.path.isdir(folder_path):
                continue
            for f in os.listdir(folder_path):
                if f.endswith((".fasta", ".fa", ".fna")):
                    fastas.append(os.path.join(folder_path, f))
                    break  # one fasta per assembler
        return fastas

    def run(self, callback=None):
        """Run prediction tools on all assembled FASTA files."""
        fastas = self._find_assembly_fastas()
        if not fastas:
            logger.warning("No assembly FASTA files found, skipping prediction")
            return {}

        results = {}

        for fasta_file in fastas:
            assembler = os.path.basename(os.path.dirname(fasta_file))
            logger.info("Running predictions on %s assembly: %s", assembler, fasta_file)

            # Prokka - gene annotation
            if callback:
                callback(f"Running Prokka on {assembler} assembly")
            prokka_out = os.path.join(self.data_dir, "predicted", "prokka", assembler)
            prokka_cmd = [
                "prokka",
                "--outdir", prokka_out,
                "--genus", self.genus,
                "--species", self.species,
                "--force", "--centre", "X", "--rfam",
            ]
            if self.proteins_file and os.path.isfile(self.proteins_file):
                prokka_cmd.extend(["--proteins", self.proteins_file])
            prokka_cmd.append(fasta_file)
            self._run_cmd(prokka_cmd, f"Prokka ({assembler})")

            # MLST - multi-locus sequence typing
            if callback:
                callback(f"Running MLST on {assembler} assembly")
            mlst_out = os.path.join(self.data_dir, "predicted", "mlst", f"{assembler}_mlst.tsv")
            mlst_cmd = ["mlst", "--quiet", fasta_file]
            mlst_result = self._run_cmd(mlst_cmd, f"MLST ({assembler})")
            if mlst_result and mlst_result.stdout:
                os.makedirs(os.path.dirname(mlst_out), exist_ok=True)
                with open(mlst_out, "w") as f:
                    f.write(mlst_result.stdout)
                results[f"mlst_{assembler}"] = mlst_result.stdout.strip()

            # Barrnap - 16S rRNA prediction
            if callback:
                callback(f"Running Barrnap on {assembler} assembly")
            barrnap_out = os.path.join(self.data_dir, "predicted", "barrnap", f"{assembler}_barrnap.gff")
            barrnap_cmd = ["barrnap", fasta_file]
            barrnap_result = self._run_cmd(barrnap_cmd, f"Barrnap ({assembler})")
            if barrnap_result and barrnap_result.stdout:
                os.makedirs(os.path.dirname(barrnap_out), exist_ok=True)
                with open(barrnap_out, "w") as f:
                    f.write(barrnap_result.stdout)

            # Abricate - antibiotic resistance gene detection
            if callback:
                callback(f"Running Abricate on {assembler} assembly")
            abricate_out = os.path.join(self.data_dir, "predicted", "abricate", f"{assembler}_abricate.tsv")
            abricate_cmd = ["abricate", fasta_file]
            abricate_result = self._run_cmd(abricate_cmd, f"Abricate ({assembler})")
            if abricate_result and abricate_result.stdout:
                os.makedirs(os.path.dirname(abricate_out), exist_ok=True)
                with open(abricate_out, "w") as f:
                    f.write(abricate_result.stdout)

            # Kleborate - only for Klebsiella
            if self.genus.lower() == "klebsiella":
                if callback:
                    callback(f"Running Kleborate on {assembler} assembly")
                kleborate_out = os.path.join(self.data_dir, "predicted", "kleborate", f"{assembler}_kleborate.txt")
                os.makedirs(os.path.dirname(kleborate_out), exist_ok=True)
                kleborate_cmd = ["kleborate", "-o", kleborate_out, "-a", fasta_file]
                self._run_cmd(kleborate_cmd, f"Kleborate ({assembler})")

            # Phigaro - phage detection
            if callback:
                callback(f"Running Phigaro on {assembler} assembly")
            phigaro_out = os.path.join(self.data_dir, "predicted", "phigaro", assembler)
            os.makedirs(phigaro_out, exist_ok=True)
            phigaro_cmd = ["phigaro", "-f", fasta_file, "-o", phigaro_out]
            self._run_cmd(phigaro_cmd, f"Phigaro ({assembler})")

            # KOFAM - functional annotation
            if callback:
                callback(f"Running KOFAM on {assembler} assembly")
            kofam_out = os.path.join(self.data_dir, "predicted", "kofam", f"{assembler}_kofam.txt")
            os.makedirs(os.path.dirname(kofam_out), exist_ok=True)
            kofam_cmd = ["exec_annotation", "-o", kofam_out, fasta_file]
            self._run_cmd(kofam_cmd, f"KOFAM ({assembler})")

        return results
