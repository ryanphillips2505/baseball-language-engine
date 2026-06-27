from detectors.source_detector import SourceType


def detect_college(text: str) -> SourceType | None:
    if (
        "ncaa baseball" in text
        or "gamecast" in text
        or "box score" in text
        or "college world series" in text
        or "espn" in text
    ):
        return SourceType.COLLEGE

    return None