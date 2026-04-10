import logging
import os

logger = logging.getLogger(__name__)


class FolderVerificationService:
    """Ensures the required directory structure exists for the pipeline."""

    def __init__(self, data_dir):
        self.data_dir = data_dir

    def run(self):
        """Create all required directories if they don't exist."""
        dirs = [
            os.path.join(self.data_dir, "input", "illumina"),
            os.path.join(self.data_dir, "input", "nanopore"),
            os.path.join(self.data_dir, "input", "pacbio"),
            os.path.join(self.data_dir, "trimmed", "illumina"),
            os.path.join(self.data_dir, "trimmed", "nanopore"),
            os.path.join(self.data_dir, "trimmed", "pacbio"),
            os.path.join(self.data_dir, "assembly", "spades"),
            os.path.join(self.data_dir, "assembly", "canu"),
            os.path.join(self.data_dir, "assembly", "flye"),
            os.path.join(self.data_dir, "assembly", "unicycler"),
            os.path.join(self.data_dir, "predicted", "prokka"),
            os.path.join(self.data_dir, "predicted", "mlst"),
            os.path.join(self.data_dir, "predicted", "barrnap"),
            os.path.join(self.data_dir, "predicted", "abricate"),
            os.path.join(self.data_dir, "predicted", "kleborate"),
            os.path.join(self.data_dir, "predicted", "kofam"),
            os.path.join(self.data_dir, "predicted", "phigaro"),
            os.path.join(self.data_dir, "reports"),
        ]
        for d in dirs:
            os.makedirs(d, exist_ok=True)
            logger.debug("Ensured directory exists: %s", d)
