from detectors.source_detector import SourceType


def detect_gamechanger(text: str) -> SourceType | None:
    has_gc_navigation = (
        "all plays" in text
        or "scoring plays" in text
        or "reverse chronological" in text
        or "get the app" in text
        or "try our family plan" in text
        or "gamechanger" in text
    )

    has_gc_innings = (
        "top 1st" in text
        or "bottom 1st" in text
        or "top 2nd" in text
        or "bottom 2nd" in text
        or "top 3rd" in text
        or "bottom 3rd" in text
    )

    has_gc_pitch_tokens = (
        "strike 1" in text
        or "strike 2" in text
        or "strike 3" in text
        or "ball 1" in text
        or "ball 2" in text
        or "ball 3" in text
        or "ball 4" in text
        or "in play" in text
    )

    if "=== pa ===" in text and has_gc_pitch_tokens:
        return SourceType.GAMECHANGER

    if has_gc_navigation and has_gc_pitch_tokens:
        return SourceType.GAMECHANGER

    if has_gc_navigation and has_gc_innings:
        return SourceType.GAMECHANGER

    return None