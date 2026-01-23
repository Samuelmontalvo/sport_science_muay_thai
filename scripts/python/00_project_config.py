from __future__ import annotations

from pathlib import Path
import logging

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
EXTERNAL_DIR = DATA_DIR / "external"
PRIVATE_DIR = DATA_DIR / "private"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
REPORTS_DIR = OUTPUTS_DIR / "reports"
MODELS_DIR = OUTPUTS_DIR / "models"
FIGURES_DIR = PROJECT_ROOT / "figures"
DOCS_DIR = PROJECT_ROOT / "docs"

COVARIATES = [
    "body_mass_change_kg",
    "sex",
    "weight_class",
    "time_between_tests_hours",
    "training_status",
]

TIMEPOINT_MAP = {"T0": 0, "T1": 1}
TIMEPOINT_LABELS = {0: "T0", 1: "T1"}


def setup_logging(level: int = logging.INFO) -> None:
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


LOGGER = logging.getLogger(__name__)


def ensure_project_dirs() -> None:
    for path in [
        RAW_DIR,
        PROCESSED_DIR,
        EXTERNAL_DIR,
        PRIVATE_DIR,
        OUTPUTS_DIR,
        REPORTS_DIR,
        MODELS_DIR,
        FIGURES_DIR,
        DOCS_DIR,
    ]:
        path.mkdir(parents=True, exist_ok=True)
