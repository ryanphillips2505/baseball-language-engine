from pathlib import Path

from dataset.dataset_registry import DATASETS


def sample_path(source: str, filename: str) -> Path:
    """
    Returns the full path to a sample dataset.

    Example:
        sample_path("gamechanger", "gamechanger_pa_blocks.txt")
    """
    return DATASETS[source] / filename