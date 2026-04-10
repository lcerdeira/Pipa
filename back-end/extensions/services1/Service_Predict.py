import logging
import os
import shutil
import subprocess

logger = logging.getLogger(__name__)


class PredictService:
    """Handles gene prediction and annotation (Prokka, MLST, Barrnap, Abricate, etc.)."""

    # All available annotation tools
    ALL_TOOLS = ["prokka", "mlst", "barrnap", "abricate", "kleborate", "phigaro", "kofam",
                 "amrfinderplus", "plasmidfinder", "mobsuite", "crisprcasfinder", "trnascan"]

    def __init__(self, data_dir, genus="Unknown", species="unknown",
                 proteins_file=None, tools=None):
        self.data_dir = data_dir
        self.genus = genus
        self.species = species
        self.proteins_file = proteins_file
        # If tools list provided, only run those; otherwise run the defaults
        self.tools = tools if tools else ["prokka", "mlst", "barrnap", "abricate"]

    def _run_cmd(self, command, description):
        tool = command[0]
        if not shutil.which(tool):
            logger.warning("%s not found in PATH, skipping %s", tool, description)
            return None
        logger.info("Running %s: %s", description, " ".join(command))
        result = subprocess.run(command, capture_output=True, text=True, timeout=7200)
        if result.returncode != 0:
            # Get last few lines of stderr for the actual error (tools like Prokka
            # write all progress to stderr, so the real error is at the end)
            stderr_lines = result.stderr.strip().splitlines()
            error_tail = "\n".join(stderr_lines[-5:]) if stderr_lines else "(no stderr)"
            logger.error("%s failed (exit %d): %s", description, result.returncode, error_tail)
            raise RuntimeError(f"{description} failed: {error_tail}")
        logger.info("%s completed successfully", description)
        return result

    @staticmethod
    def _clean_fasta_headers(fasta_path):
        """Rename FASTA headers to short contig names (contig_NNN) for Prokka compatibility."""
        cleaned = fasta_path + ".cleaned"
        count = 0
        with open(fasta_path) as fin, open(cleaned, "w") as fout:
            for line in fin:
                if line.startswith(">"):
                    count += 1
                    fout.write(f">contig_{count}\n")
                else:
                    fout.write(line)
        logger.info("Cleaned %d contig headers in %s", count, fasta_path)
        return cleaned

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
                    fpath = os.path.join(folder_path, f)
                    if os.path.getsize(fpath) > 0:
                        fastas.append(fpath)
                        break  # one fasta per assembler
        return fastas

    def _should_run(self, tool_key):
        """Check if a tool should be run based on the tools list."""
        return tool_key in self.tools

    def run(self, callback=None):
        """Run selected prediction tools on all assembled FASTA files."""
        fastas = self._find_assembly_fastas()
        if not fastas:
            logger.warning("No assembly FASTA files found, skipping prediction")
            return {}

        logger.info("Tools to run: %s", ", ".join(self.tools))
        results = {}

        for fasta_file in fastas:
            assembler = os.path.basename(os.path.dirname(fasta_file))
            logger.info("Running predictions on %s assembly: %s", assembler, fasta_file)

            # Clean FASTA headers for Prokka compatibility
            cleaned_fasta = self._clean_fasta_headers(fasta_file)

            # Prokka - gene annotation
            if self._should_run("prokka"):
                if callback:
                    callback(f"Running Prokka on {assembler} assembly")
                prokka_out = os.path.join(self.data_dir, "predicted", "prokka", assembler)
                prokka_cmd = [
                    "prokka",
                    "--outdir", prokka_out,
                    "--genus", self.genus,
                    "--species", self.species,
                    "--force", "--rfam",
                    "--locustag", "PIPA",
                    "--prefix", assembler,
                ]
                if self.proteins_file and os.path.isfile(self.proteins_file):
                    prokka_cmd.extend(["--proteins", self.proteins_file])
                prokka_cmd.append(cleaned_fasta)
                self._run_cmd(prokka_cmd, f"Prokka ({assembler})")

            # MLST - multi-locus sequence typing
            if self._should_run("mlst"):
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
            if self._should_run("barrnap"):
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
            if self._should_run("abricate"):
                if callback:
                    callback(f"Running Abricate on {assembler} assembly")
                abricate_out = os.path.join(self.data_dir, "predicted", "abricate", f"{assembler}_abricate.tsv")
                abricate_cmd = ["abricate", fasta_file]
                abricate_result = self._run_cmd(abricate_cmd, f"Abricate ({assembler})")
                if abricate_result and abricate_result.stdout:
                    os.makedirs(os.path.dirname(abricate_out), exist_ok=True)
                    with open(abricate_out, "w") as f:
                        f.write(abricate_result.stdout)

            # AMRFinderPlus - NCBI AMR detection
            if self._should_run("amrfinderplus"):
                if callback:
                    callback(f"Running AMRFinderPlus on {assembler} assembly")
                amr_out = os.path.join(self.data_dir, "predicted", "amrfinderplus", f"{assembler}_amrfinder.tsv")
                os.makedirs(os.path.dirname(amr_out), exist_ok=True)
                amr_cmd = ["amrfinder", "-n", fasta_file, "-o", amr_out]
                self._run_cmd(amr_cmd, f"AMRFinderPlus ({assembler})")

            # PlasmidFinder
            if self._should_run("plasmidfinder"):
                if callback:
                    callback(f"Running PlasmidFinder on {assembler} assembly")
                pf_out = os.path.join(self.data_dir, "predicted", "plasmidfinder", assembler)
                os.makedirs(pf_out, exist_ok=True)
                pf_cmd = ["plasmidfinder.py", "-i", fasta_file, "-o", pf_out]
                self._run_cmd(pf_cmd, f"PlasmidFinder ({assembler})")

            # MOB-suite - plasmid typing
            if self._should_run("mobsuite"):
                if callback:
                    callback(f"Running MOB-suite on {assembler} assembly")
                mob_out = os.path.join(self.data_dir, "predicted", "mobsuite", assembler)
                os.makedirs(mob_out, exist_ok=True)
                mob_cmd = ["mob_recon", "-i", fasta_file, "-o", mob_out]
                self._run_cmd(mob_cmd, f"MOB-suite ({assembler})")

            # CRISPRCasFinder
            if self._should_run("crisprcasfinder"):
                if callback:
                    callback(f"Running CRISPRCasFinder on {assembler} assembly")
                crispr_out = os.path.join(self.data_dir, "predicted", "crisprcasfinder", assembler)
                os.makedirs(crispr_out, exist_ok=True)
                crispr_cmd = ["CRISPRCasFinder.pl", "-in", fasta_file, "-out", crispr_out]
                self._run_cmd(crispr_cmd, f"CRISPRCasFinder ({assembler})")

            # tRNAscan-SE
            if self._should_run("trnascan"):
                if callback:
                    callback(f"Running tRNAscan-SE on {assembler} assembly")
                trna_out = os.path.join(self.data_dir, "predicted", "trnascan", f"{assembler}_trnascan.txt")
                os.makedirs(os.path.dirname(trna_out), exist_ok=True)
                trna_cmd = ["tRNAscan-SE", "-B", "-o", trna_out, fasta_file]
                self._run_cmd(trna_cmd, f"tRNAscan-SE ({assembler})")

            # Kleborate - only for Klebsiella
            if self._should_run("kleborate") and self.genus.lower() == "klebsiella":
                if callback:
                    callback(f"Running Kleborate on {assembler} assembly")
                kleborate_out = os.path.join(self.data_dir, "predicted", "kleborate", f"{assembler}_kleborate.txt")
                os.makedirs(os.path.dirname(kleborate_out), exist_ok=True)
                kleborate_cmd = ["kleborate", "-o", kleborate_out, "-a", fasta_file]
                self._run_cmd(kleborate_cmd, f"Kleborate ({assembler})")

            # Phigaro - phage detection
            if self._should_run("phigaro"):
                if callback:
                    callback(f"Running Phigaro on {assembler} assembly")
                phigaro_out = os.path.join(self.data_dir, "predicted", "phigaro", assembler)
                os.makedirs(phigaro_out, exist_ok=True)
                phigaro_cmd = ["phigaro", "-f", fasta_file, "-o", phigaro_out]
                self._run_cmd(phigaro_cmd, f"Phigaro ({assembler})")

            # KOFAM - functional annotation
            if self._should_run("kofam"):
                if callback:
                    callback(f"Running KOFAM on {assembler} assembly")
                kofam_out = os.path.join(self.data_dir, "predicted", "kofam", f"{assembler}_kofam.txt")
                os.makedirs(os.path.dirname(kofam_out), exist_ok=True)
                kofam_cmd = ["exec_annotation", "-o", kofam_out, fasta_file]
                self._run_cmd(kofam_cmd, f"KOFAM ({assembler})")

        return results
