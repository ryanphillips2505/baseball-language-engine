import re
from enum import Enum


class SourceType(str, Enum):
    GAMECHANGER = "gamechanger"
    ISCORE = "iscore"
    MLB = "mlb"
    COLLEGE = "college"
    UNKNOWN = "unknown"


def detect_source(raw_text: str) -> SourceType:
    text = raw_text.lower()

    # iScore uses numbered batter/event lines.
    if re.search(r"#\d+\s+[a-z]", text):
        return SourceType.ISCORE

    # ESPN / college samples often contain NCAA-style result language.
    if (
        "struck out swinging." in text
        or "struck out looking." in text
        or "reached on bunt single" in text
    ):
        return SourceType.COLLEGE

    # GameChanger exports usually contain app navigation/play list language.
    if (
        "all plays" in text
        or "scoring plays" in text
        or "top 1st" in text
        or "bottom 1st" in text
    ):
        return SourceType.GAMECHANGER

    # MLB Gameday language.
    if (
        "mlb.com" in text
        or "statcast" in text
        or "called out on strikes" in text
        or "grounds out to" in text
        or "flies out to" in text
        or "homers to" in text
    ):
        return SourceType.MLB

    return SourceType.UNKNOWN