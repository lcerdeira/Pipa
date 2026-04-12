FROM mambaorg/micromamba:1.5-jammy

USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl git wget build-essential && \
    rm -rf /var/lib/apt/lists/*
USER $MAMBA_USER

# Stage 1: Install core tools via conda (known to resolve)
RUN micromamba install -y -n base -c conda-forge -c bioconda -c defaults \
    python=3.10 \
    flask flask-cors werkzeug pip git \
    # Trimming
    trim-galore porechop_abi \
    # Assembly
    "spades>=4.0" flye canu \
    # Core annotation
    prokka mlst barrnap abricate \
    ncbi-amrfinderplus trnascan-se \
    # Assembly QC
    quast \
    # Utilities
    samtools bcftools \
    && micromamba clean --all --yes

# Stage 2: Additional bioconda tools (one by one, skip on failure)
RUN for tool in \
    bakta eggnog-mapper kofamscan busco checkm-genome \
    plasmidfinder mob_suite phigaro phispy ismapper \
    kleborate staphopia-sccmec ectyper emmtyper genotyphi \
    hicap hpsuissero legsta lissero meningotype ngmaster \
    pasty pbptyper sccmec seqsero2 sistr_cmd spatyper stecfinder; do \
    echo "Installing $tool..." && \
    micromamba install -y -n base -c conda-forge -c bioconda "$tool" 2>/dev/null \
    || echo "SKIP: $tool (conflict or not available)"; \
    done && micromamba clean --all --yes

# Stage 3: pip installs for tools with conda conflicts
RUN micromamba run -n base pip install --no-cache-dir \
    defense-finder-cli \
    mcroni \
    shigapass \
    clermontyping \
    tb-profiler \
    shigatyper \
    shigeifinder \
    "git+https://github.com/rrwick/Unicycler.git" \
    "git+https://github.com/sanger-pathogens/seroba.git" \
    "git+https://github.com/jimmyliu1326/SsuisSero.git" \
    || echo "Some pip installs failed, continuing"

# Update AMRFinderPlus database
RUN micromamba run -n base amrfinder --update || true

# Copy backend code
COPY --chown=$MAMBA_USER:$MAMBA_USER back-end/ /app/

WORKDIR /app
RUN mkdir -p /data

ENV PIPA_DATA_DIR=/data
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["micromamba", "run", "-n", "base", "python", "-m", "flask", "run", "--host", "0.0.0.0", "--port", "5000"]
