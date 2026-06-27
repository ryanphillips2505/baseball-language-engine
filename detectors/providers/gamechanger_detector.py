from detectors.source_detector import SourceType


def detect_gamechanger(text: str) -> SourceType | None:
    if "=== pa ===" in text:
        if (
            "strike 1" in text
            or "strike 2" in text
            or "strike 3" in text
            or "ball 1" in text
            or "ball 2" in text
            or "ball 3" in text
            or "ball 4" in text
            or "in play" in text
        ):
            return SourceType.GAMECHANGER

    if (
        "all plays" in text
        or "scoring plays" in text
        or "top 1st" in text
        or "bottom 1st" in text
    ):
        return SourceType.GAMECHANGER

    return None