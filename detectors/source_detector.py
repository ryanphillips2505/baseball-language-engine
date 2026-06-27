import re
from enum import Enum


class SourceType(str, Enum):
    GAMECHANGER = "gamechanger"
    ISCORE = "iscore"
    MLB = "mlb"
    COLLEGE = "college"
    UNKNOWN = "unknown"


def detect_source(raw_text: str) -> SourceType:
    if not raw_text:
        return SourceType.UNKNOWN

    text = raw_text.lower()

    if "iscoresports.com" in text or re.search(r"\(\d+\)\s+#\d+", text):
        return SourceType.ISCORE

    if (
        "ncaa baseball" in text
        or "gamecast" in text
        or "box score" in text
        or "college world series" in text
        or "espn" in text
    ):
        return SourceType.COLLEGE

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

        return SourceType.MLB

    if (
        "all plays" in text
        or "scoring plays" in text
        or "top 1st" in text
        or "bottom 1st" in text
    ):
        return SourceType.GAMECHANGER

    return SourceType.UNKNOWN