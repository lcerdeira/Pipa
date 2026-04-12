import logging
import os
import shutil
import subprocess

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Tool Registry — every annotation tool is defined here as a dict.
# The generic runner iterates this list; no per-tool if-blocks needed.
# ---------------------------------------------------------------------------

TOOL_REGISTRY = [
    # ── General Annotation ─────────────────────────────────────────────────
    {
        "key": "prokka", "name": "Prokka", "category": "general_annotation",
        "command": "prokka", "build_cmd": "_build_prokka_cmd",
        "description": "Gene annotation",
    },
    {
        "key": "bakta", "name": "Bakta", "category": "general_annotation",
        "command": "bakta", "build_cmd": "_build_bakta_cmd",
        "description": "Rapid bacterial annotation",
    },
    {
        "key": "mlst", "name": "MLST", "category": "general_annotation",
        "command": "mlst",
        "args_template": ["--quiet", "{fasta}"],
        "output_pattern": "{tool_dir}/{assembler}_mlst.tsv",
        "capture_stdout": True,
        "description": "Sequence typing",
    },
    {
        "key": "barrnap", "name": "Barrnap", "category": "general_annotation",
        "command": "barrnap",
        "args_template": ["{fasta}"],
        "output_pattern": "{tool_dir}/{assembler}_barrnap.gff",
        "capture_stdout": True,
        "description": "Ribosomal RNA",
    },
    {
        "key": "trnascan", "name": "tRNAscan-SE", "category": "general_annotation",
        "command": "tRNAscan-SE",
        "args_template": ["-B", "-o", "{tool_dir}/{assembler}_trnascan.txt", "{fasta}"],
        "output_pattern": "{tool_dir}/{assembler}_trnascan.txt",
        "description": "tRNA prediction",
    },
    {
        "key": "eggnog", "name": "EggNOG-mapper", "category": "general_annotation",
        "command": "emapper.py",
        "args_template": ["-i", "{fasta}", "--itype", "genome", "-o", "{assembler}", "--output_dir", "{tool_dir}", "--cpu", "4"],
        "output_pattern": "{tool_dir}/{assembler}.emapper.annotations",
        "description": "Functional annotation (orthologous groups)",
    },
    {
        "key": "kofam", "name": "KOFAM", "category": "general_annotation",
        "command": "exec_annotation",
        "args_template": ["-o", "{tool_dir}/{assembler}_kofam.txt", "{fasta}"],
        "output_pattern": "{tool_dir}/{assembler}_kofam.txt",
        "description": "KEGG annotation",
    },

    # ── Assembly Quality ───────────────────────────────────────────────────
    {
        "key": "busco", "name": "BUSCO", "category": "assembly_quality",
        "command": "busco",
        "args_template": ["-i", "{fasta}", "-o", "{assembler}", "--out_path", "{tool_dir}", "-m", "genome", "--auto-lineage-prok", "-c", "4", "-f"],
        "output_pattern": "{tool_dir}/{assembler}/",
        "description": "Assembly completeness",
    },
    {
        "key": "checkm", "name": "CheckM", "category": "assembly_quality",
        "command": "checkm",
        "args_template": ["lineage_wf", "-x", "fasta", "{fasta_dir}", "{tool_dir}/{assembler}"],
        "output_pattern": "{tool_dir}/{assembler}/",
        "description": "Quality assessment",
    },
    {
        "key": "quast", "name": "QUAST", "category": "assembly_quality",
        "command": "quast",
        "args_template": ["{fasta}", "-o", "{tool_dir}/{assembler}"],
        "output_pattern": "{tool_dir}/{assembler}/",
        "description": "Contig quality",
    },

    # ── Resistance & Virulence ─────────────────────────────────────────────
    {
        "key": "abricate", "name": "Abricate", "category": "resistance",
        "command": "abricate",
        "args_template": ["{fasta}"],
        "output_pattern": "{tool_dir}/{assembler}_abricate.tsv",
        "capture_stdout": True,
        "description": "Resistance genes",
    },
    {
        "key": "abricate_vfdb", "name": "Abricate (VFDB)", "category": "resistance",
        "command": "abricate",
        "args_template": ["--db", "vfdb", "{fasta}"],
        "output_pattern": "{tool_dir}/{assembler}_abricate_vfdb.tsv",
        "capture_stdout": True,
        "description": "Virulence factors (VFDB)",
    },
    {
        "key": "amrfinderplus", "name": "AMRFinderPlus", "category": "resistance",
        "command": "amrfinder",
        "args_template": ["-n", "{fasta}", "-o", "{tool_dir}/{assembler}_amrfinder.tsv"],
        "output_pattern": "{tool_dir}/{assembler}_amrfinder.tsv",
        "description": "AMR detection (NCBI)",
    },
    {
        "key": "mcroni", "name": "mcroni", "category": "resistance",
        "command": "mcroni",
        "args_template": ["-i", "{fasta}", "-o", "{tool_dir}/{assembler}_mcroni.tsv"],
        "output_pattern": "{tool_dir}/{assembler}_mcroni.tsv",
        "description": "Colistin resistance (mcr-1)",
    },

    # ── Mobile Elements & Defense ──────────────────────────────────────────
    {
        "key": "plasmidfinder", "name": "PlasmidFinder", "category": "mobile_elements",
        "command": "plasmidfinder.py",
        "args_template": ["-i", "{fasta}", "-o", "{tool_dir}/{assembler}"],
        "output_pattern": "{tool_dir}/{assembler}/",
        "description": "Plasmid replicons",
    },
    {
        "key": "mobsuite", "name": "MOB-suite", "category": "mobile_elements",
        "command": "mob_recon",
        "args_template": ["-i", "{fasta}", "-o", "{tool_dir}/{assembler}"],
        "output_pattern": "{tool_dir}/{assembler}/",
        "description": "Plasmid typing",
    },
    {
        "key": "phigaro", "name": "Phigaro", "category": "mobile_elements",
        "command": "phigaro",
        "args_template": ["-f", "{fasta}", "-o", "{tool_dir}/{assembler}"],
        "output_pattern": "{tool_dir}/{assembler}/",
        "description": "Phage detection",
    },
    {
        "key": "phispy", "name": "PhiSpy", "category": "mobile_elements",
        "command": "PhiSpy.py",
        "args_template": ["{fasta}", "-o", "{tool_dir}/{assembler}"],
        "output_pattern": "{tool_dir}/{assembler}/",
        "description": "Prophage prediction",
    },
    {
        "key": "crisprcasfinder", "name": "CRISPRCasFinder", "category": "mobile_elements",
        "command": "CRISPRCasFinder.pl",
        "args_template": ["-in", "{fasta}", "-out", "{tool_dir}/{assembler}"],
        "output_pattern": "{tool_dir}/{assembler}/",
        "description": "CRISPR arrays",
    },
    {
        "key": "defensefinder", "name": "DefenseFinder", "category": "mobile_elements",
        "command": "defense-finder",
        "args_template": ["run", "--workers", "4", "-o", "{tool_dir}/{assembler}", "{fasta}"],
        "output_pattern": "{tool_dir}/{assembler}/",
        "description": "Anti-phage systems",
    },
    {
        "key": "ismapper", "name": "ISMapper", "category": "mobile_elements",
        "command": "ismap",
        "args_template": ["--queries", "{fasta}", "--output", "{tool_dir}/{assembler}"],
        "output_pattern": "{tool_dir}/{assembler}/",
        "description": "Insertion sites",
    },

    # ── Organism-Specific Typing ───────────────────────────────────────────
    {
        "key": "kleborate", "name": "Kleborate", "category": "organism_typing",
        "command": "kleborate",
        "args_template": ["--assemblies", "{fasta}", "-o", "{tool_dir}/{assembler}_kleborate.txt"],
        "output_pattern": "{tool_dir}/{assembler}_kleborate.txt",
        "description": "Klebsiella typing",
    },
    {
        "key": "staphtyper", "name": "staphtyper", "category": "organism_typing",
        "command": "staphtyper",
        "args_template": ["--input", "{fasta}", "--prefix", "{tool_dir}/{assembler}"],
        "output_pattern": "{tool_dir}/{assembler}.tsv",
        "organism_filter": {"genus": "staphylococcus"},
        "description": "S. aureus agr/spa/SCCmec typing",
    },
    {
        "key": "tbprofiler", "name": "TBProfiler", "category": "organism_typing",
        "command": "tb-profiler",
        "args_template": ["profile", "-a", "{fasta}", "--prefix", "{assembler}", "--dir", "{tool_dir}"],
        "output_pattern": "{tool_dir}/results/{assembler}.results.json",
        "organism_filter": {"genus": "mycobacterium"},
        "description": "M. tuberculosis resistance/lineage",
    },
    {
        "key": "clermontyping", "name": "ClermonTyping", "category": "organism_typing",
        "command": "clermonTyping.sh",
        "args_template": ["--fasta", "{fasta}", "--name", "{assembler}"],
        "output_pattern": "{tool_dir}/{assembler}/",
        "organism_filter": {"genus": "escherichia"},
        "description": "E. coli phylotyping",
    },
    {
        "key": "ectyper", "name": "ECTyper", "category": "organism_typing",
        "command": "ectyper",
        "args_template": ["-i", "{fasta}", "-o", "{tool_dir}/{assembler}"],
        "output_pattern": "{tool_dir}/{assembler}/",
        "organism_filter": {"genus": "escherichia"},
        "description": "E. coli serotyping",
    },
    {
        "key": "emmtyper", "name": "emmtyper", "category": "organism_typing",
        "command": "emmtyper",
        "args_template": ["{fasta}"],
        "output_pattern": "{tool_dir}/{assembler}_emmtyper.tsv",
        "capture_stdout": True,
        "organism_filter": {"genus": "streptococcus"},
        "description": "S. pyogenes emm-typing",
    },
    {
        "key": "genotyphi", "name": "GenoTyphi", "category": "organism_typing",
        "command": "genotyphi",
        "args_template": ["--mode", "assembly", "--assembly", "{fasta}", "--output", "{tool_dir}/{assembler}_genotyphi.tsv"],
        "output_pattern": "{tool_dir}/{assembler}_genotyphi.tsv",
        "organism_filter": {"genus": "salmonella"},
        "description": "S. Typhi genotyping",
    },
    {
        "key": "hicap", "name": "hicap", "category": "organism_typing",
        "command": "hicap",
        "args_template": ["--query_fp", "{fasta}", "--output_dir", "{tool_dir}/{assembler}"],
        "output_pattern": "{tool_dir}/{assembler}/",
        "organism_filter": {"genus": "haemophilus"},
        "description": "H. influenzae cap locus",
    },
    {
        "key": "hpsuissero", "name": "HpSuisSero", "category": "organism_typing",
        "command": "hpsuissero",
        "args_template": ["-i", "{fasta}", "-o", "{tool_dir}/{assembler}_hpsuissero.tsv"],
        "output_pattern": "{tool_dir}/{assembler}_hpsuissero.tsv",
        "organism_filter": {"genus": "haemophilus"},
        "description": "H. parasuis serotyping",
    },
    {
        "key": "legsta", "name": "legsta", "category": "organism_typing",
        "command": "legsta",
        "args_template": ["{fasta}"],
        "output_pattern": "{tool_dir}/{assembler}_legsta.tsv",
        "capture_stdout": True,
        "organism_filter": {"genus": "legionella"},
        "description": "L. pneumophila typing",
    },
    {
        "key": "lissero", "name": "LisSero", "category": "organism_typing",
        "command": "lissero",
        "args_template": ["{fasta}"],
        "output_pattern": "{tool_dir}/{assembler}_lissero.tsv",
        "capture_stdout": True,
        "organism_filter": {"genus": "listeria"},
        "description": "L. monocytogenes serogroup",
    },
    {
        "key": "meningotype", "name": "meningotype", "category": "organism_typing",
        "command": "meningotype",
        "args_template": ["{fasta}"],
        "output_pattern": "{tool_dir}/{assembler}_meningotype.tsv",
        "capture_stdout": True,
        "organism_filter": {"genus": "neisseria"},
        "description": "N. meningitidis serotyping",
    },
    {
        "key": "ngmaster", "name": "ngmaster", "category": "organism_typing",
        "command": "ngmaster",
        "args_template": ["{fasta}"],
        "output_pattern": "{tool_dir}/{assembler}_ngmaster.tsv",
        "capture_stdout": True,
        "organism_filter": {"genus": "neisseria"},
        "description": "N. gonorrhoeae MAST",
    },
    {
        "key": "pasty", "name": "pasty", "category": "organism_typing",
        "command": "pasty",
        "args_template": ["-i", "{fasta}", "-o", "{tool_dir}/{assembler}"],
        "output_pattern": "{tool_dir}/{assembler}/",
        "organism_filter": {"genus": "pseudomonas"},
        "description": "P. aeruginosa serogrouping",
    },
    {
        "key": "pbptyper", "name": "pbptyper", "category": "organism_typing",
        "command": "pbptyper",
        "args_template": ["--assembly", "{fasta}", "--prefix", "{assembler}", "--outdir", "{tool_dir}"],
        "output_pattern": "{tool_dir}/{assembler}.tsv",
        "organism_filter": {"genus": "streptococcus"},
        "description": "S. pneumoniae PBP typing",
    },
    {
        "key": "pneumocat", "name": "PneumoCaT", "category": "organism_typing",
        "command": "pneumocat",
        "args_template": ["-i", "{fasta}", "-o", "{tool_dir}/{assembler}"],
        "output_pattern": "{tool_dir}/{assembler}/",
        "organism_filter": {"genus": "streptococcus"},
        "description": "S. pneumoniae capsular typing",
    },
    {
        "key": "sccmec", "name": "sccmec", "category": "organism_typing",
        "command": "sccmec",
        "args_template": ["--input", "{fasta}", "--prefix", "{tool_dir}/{assembler}"],
        "output_pattern": "{tool_dir}/{assembler}.tsv",
        "organism_filter": {"genus": "staphylococcus"},
        "description": "SCCmec cassette typing",
    },
    {
        "key": "seqsero2", "name": "SeqSero2", "category": "organism_typing",
        "command": "SeqSero2_package.py",
        "args_template": ["-m", "k", "-t", "4", "-i", "{fasta}", "-d", "{tool_dir}/{assembler}"],
        "output_pattern": "{tool_dir}/{assembler}/",
        "organism_filter": {"genus": "salmonella"},
        "description": "Salmonella serotype prediction",
    },
    {
        "key": "seroba", "name": "SeroBA", "category": "organism_typing",
        "command": "seroba",
        "args_template": ["runSerotyping", "{fasta}", "{tool_dir}/{assembler}"],
        "output_pattern": "{tool_dir}/{assembler}/",
        "organism_filter": {"genus": "streptococcus"},
        "description": "S. pneumoniae serotyping",
    },
    {
        "key": "shigapass", "name": "ShigaPass", "category": "organism_typing",
        "command": "shigapass",
        "args_template": ["-i", "{fasta}", "-o", "{tool_dir}/{assembler}"],
        "output_pattern": "{tool_dir}/{assembler}/",
        "organism_filter": {"genus": "shigella"},
        "description": "Shigella serotyping",
    },
    {
        "key": "shigatyper", "name": "ShigaTyper", "category": "organism_typing",
        "command": "shigatyper",
        "args_template": ["--SE", "{fasta}"],
        "output_pattern": "{tool_dir}/{assembler}_shigatyper.tsv",
        "capture_stdout": True,
        "organism_filter": {"genus": "shigella"},
        "description": "Shigella serotype",
    },
    {
        "key": "shigeifinder", "name": "ShigEiFinder", "category": "organism_typing",
        "command": "shigeifinder",
        "args_template": ["-i", "{fasta}", "-o", "{tool_dir}/{assembler}_shigeifinder.tsv"],
        "output_pattern": "{tool_dir}/{assembler}_shigeifinder.tsv",
        "organism_filter": {"genus": "shigella"},
        "description": "Shigella/EIEC serotyping",
    },
    {
        "key": "sistr", "name": "SISTR", "category": "organism_typing",
        "command": "sistr",
        "args_template": ["-i", "{fasta}", "-o", "{tool_dir}/{assembler}_sistr.tsv", "-f", "tab"],
        "output_pattern": "{tool_dir}/{assembler}_sistr.tsv",
        "organism_filter": {"genus": "salmonella"},
        "description": "Salmonella serovar prediction",
    },
    {
        "key": "spatyper", "name": "spaTyper", "category": "organism_typing",
        "command": "spaTyper",
        "args_template": ["-i", "{fasta}"],
        "output_pattern": "{tool_dir}/{assembler}_spatyper.tsv",
        "capture_stdout": True,
        "organism_filter": {"genus": "staphylococcus"},
        "description": "S. aureus spa typing",
    },
    {
        "key": "ssuissero", "name": "SsuisSero", "category": "organism_typing",
        "command": "ssuissero",
        "args_template": ["-i", "{fasta}", "-o", "{tool_dir}/{assembler}_ssuissero.tsv"],
        "output_pattern": "{tool_dir}/{assembler}_ssuissero.tsv",
        "organism_filter": {"genus": "streptococcus"},
        "description": "S. suis serotyping",
    },
    {
        "key": "staphopiasccmec", "name": "staphopia-sccmec", "category": "organism_typing",
        "command": "staphopia-sccmec",
        "args_template": ["--input", "{fasta}"],
        "output_pattern": "{tool_dir}/{assembler}_staphopiasccmec.tsv",
        "capture_stdout": True,
        "organism_filter": {"genus": "staphylococcus"},
        "description": "S. aureus SCCmec typing",
    },
    {
        "key": "stecfinder", "name": "STECFinder", "category": "organism_typing",
        "command": "stecfinder",
        "args_template": ["-i", "{fasta}", "-o", "{tool_dir}/{assembler}_stecfinder.tsv"],
        "output_pattern": "{tool_dir}/{assembler}_stecfinder.tsv",
        "organism_filter": {"genus": "escherichia"},
        "description": "STEC serotyping",
    },
]

# Build lookup structures
ALL_TOOL_KEYS = [t["key"] for t in TOOL_REGISTRY]
DEFAULT_TOOLS = ["prokka", "mlst", "barrnap", "abricate"]


class PredictService:
    """Data-driven annotation service. Tools are defined in TOOL_REGISTRY."""

    def __init__(self, data_dir, genus="Unknown", species="unknown",
                 proteins_file=None, tools=None):
        self.data_dir = data_dir
        self.genus = genus
        self.species = species
        self.proteins_file = proteins_file
        self.tools = tools if tools else DEFAULT_TOOLS

    def _run_cmd(self, command, description):
        tool = command[0]
        if not shutil.which(tool):
            logger.warning("%s not found in PATH, skipping %s", tool, description)
            return None
        logger.info("Running %s: %s", description, " ".join(command))
        result = subprocess.run(command, capture_output=True, text=True, timeout=7200)
        if result.returncode != 0:
            stderr_lines = result.stderr.strip().splitlines()
            error_tail = "\n".join(stderr_lines[-5:]) if stderr_lines else "(no stderr)"
            logger.error("%s failed (exit %d): %s", description, result.returncode, error_tail)
            raise RuntimeError(f"{description} failed: {error_tail}")
        logger.info("%s completed successfully", description)
        return result

    @staticmethod
    def _clean_fasta_headers(fasta_path):
        """Rename FASTA headers to short contig names for tool compatibility."""
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
        """Find all non-empty .fasta files across assembly output directories."""
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
                        break
        return fastas

    def _should_run(self, tool_key):
        return tool_key in self.tools

    def _organism_matches(self, tool_def):
        filt = tool_def.get("organism_filter")
        if not filt:
            return True
        if "genus" in filt and self.genus.lower() != filt["genus"].lower():
            return False
        if "species" in filt and self.species.lower() != filt["species"].lower():
            return False
        return True

    def _substitute_args(self, args_template, fasta, assembler, tool_dir):
        """Replace placeholders in args template."""
        fasta_dir = os.path.dirname(fasta)
        result = []
        for arg in args_template:
            result.append(
                arg.replace("{fasta}", fasta)
                   .replace("{assembler}", assembler)
                   .replace("{tool_dir}", tool_dir)
                   .replace("{fasta_dir}", fasta_dir)
            )
        return result

    def _resolve_output_path(self, tool_def, assembler, tool_dir):
        pattern = tool_def.get("output_pattern", "{tool_dir}/{assembler}.txt")
        return (pattern.replace("{tool_dir}", tool_dir)
                       .replace("{assembler}", assembler))

    # ── Complex tool builders ──────────────────────────────────────────────

    def _build_prokka_cmd(self, tool_def, fasta, cleaned_fasta, assembler, tool_dir):
        out_dir = os.path.join(tool_dir, assembler)
        cmd = [
            "prokka", "--outdir", out_dir,
            "--genus", self.genus, "--species", self.species,
            "--force", "--rfam", "--locustag", "PIPA", "--prefix", assembler,
        ]
        if self.proteins_file and os.path.isfile(self.proteins_file):
            cmd.extend(["--proteins", self.proteins_file])
        cmd.append(cleaned_fasta)
        return cmd, out_dir

    def _build_bakta_cmd(self, tool_def, fasta, cleaned_fasta, assembler, tool_dir):
        out_dir = os.path.join(tool_dir, assembler)
        cmd = [
            "bakta", cleaned_fasta,
            "--output", out_dir,
            "--genus", self.genus, "--species", self.species,
            "--prefix", assembler, "--force", "--threads", "4",
        ]
        db_path = os.environ.get("BAKTA_DB")
        if db_path:
            cmd.extend(["--db", db_path])
        return cmd, out_dir

    # ── Main runner ────────────────────────────────────────────────────────

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
            cleaned_fasta = self._clean_fasta_headers(fasta_file)

            for tool_def in TOOL_REGISTRY:
                key = tool_def["key"]
                if not self._should_run(key):
                    continue
                if not self._organism_matches(tool_def):
                    logger.info("Skipping %s (organism filter: %s, current: %s %s)",
                                tool_def["name"], tool_def.get("organism_filter"),
                                self.genus, self.species)
                    continue

                if callback:
                    callback(f"Running {tool_def['name']} on {assembler} assembly")

                tool_dir = os.path.join(self.data_dir, "predicted", key)
                os.makedirs(tool_dir, exist_ok=True)

                try:
                    if "build_cmd" in tool_def:
                        cmd, output = getattr(self, tool_def["build_cmd"])(
                            tool_def, fasta_file, cleaned_fasta, assembler, tool_dir)
                    else:
                        fasta_input = cleaned_fasta if tool_def.get("use_cleaned") else fasta_file
                        cmd = [tool_def["command"]] + self._substitute_args(
                            tool_def["args_template"], fasta_input, assembler, tool_dir)
                        output = self._resolve_output_path(tool_def, assembler, tool_dir)

                    # Ensure output directory exists
                    out_dir = os.path.dirname(output) if not output.endswith("/") else output
                    os.makedirs(out_dir, exist_ok=True)

                    result = self._run_cmd(cmd, f"{tool_def['name']} ({assembler})")

                    # Write stdout to file for capture_stdout tools
                    if tool_def.get("capture_stdout") and result and result.stdout:
                        with open(output, "w") as f:
                            f.write(result.stdout)
                        if key.startswith("mlst"):
                            results[f"mlst_{assembler}"] = result.stdout.strip()

                except Exception as e:
                    logger.error("%s failed: %s", tool_def["name"], e)

        return results
