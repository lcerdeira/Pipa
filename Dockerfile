FROM mambaorg/micromamba:1.5-jammy

USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl git wget && \
    rm -rf /var/lib/apt/lists/*
USER $MAMBA_USER

# Copy environment file and create the conda environment
COPY --chown=$MAMBA_USER:$MAMBA_USER environment.yml /tmp/environment.yml
RUN micromamba install -y -n base -f /tmp/environment.yml && \
    micromamba clean --all --yes

# Update AMRFinderPlus database
RUN micromamba run -n base amrfinder --update || true

# Copy backend code
COPY --chown=$MAMBA_USER:$MAMBA_USER back-end/ /app/

WORKDIR /app

# Create default data directory
RUN mkdir -p /data

ENV PIPA_DATA_DIR=/data
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["micromamba", "run", "-n", "base", "python", "-m", "flask", "run", "--host", "0.0.0.0", "--port", "5000"]
