from detectors.source_detector import SourceType


def detect_mlb(text: str) -> SourceType | None:
    if "=== pa ===" in text:
        return SourceType.MLB

    return None