from __future__ import annotations

import re
from enum import Enum


class SourceType(str, Enum):
    GAMECHANGER = "gamechanger"
    ISCORE = "iscore"
    MLB = "mlb"
    COLLEGE = "college"
    UNKNOWN = "unknown"


def _looks_like_gamechanger_cleaned_blocks(text: str) -> bool:
    return (
        "=== pa ===" in text
        and "=== end ===" in text
        and (
            re.search(r"\bball\s+\d\b", text)
            or re.search(r"\bstrike\s+\d\b", text)
            or "in play." in text
            or " pitching." in text
            or " pitching," in text
        )
    )


def _looks_like_mlb_cleaned_blocks(text: str) -> bool:
    return (
        "=== pa ===" in text
        and "=== end ===" in text
        and not _looks_like_gamechanger_cleaned_blocks(text)
        and (
            re.search(r"\b\w[\w'. -]+ strikes out\b", text)
            or re.search(r"\b\w[\w'. -]+ singles\b", text)
            or re.search(r"\b\w[\w'. -]+ doubles\b", text)
            or re.search(r"\b\w[\w'. -]+ triples\b", text)
            or re.search(r"\b\w[\w'. -]+ homers\b", text)
            or re.search(r"\b\w[\w'. -]+ walks\.", text)
            or re.search(r"\b\w[\w'. -]+ grounds out\b", text)
            or re.search(r"\b\w[\w'. -]+ flies out\b", text)
            or re.search(r"\b\w[\w'. -]+ lines out\b", text)
        )
    )


def _looks_like_espn_college_raw_text(text: str) -> bool:
    college_markers = (
        "men's college world series",
        "college world series",
        "ncaa baseball",
        "college baseball",
    )

    espn_page_markers = (
        "play-by-play" in text
        and "all plays" in text
        and (
            "gamecast" in text
            or "box score" in text
            or any(marker in text for marker in college_markers)
        )
    )

    explicit_espn = (
        "espn" in text
        and (
            "play-by-play" in text
            or any(marker in text for marker in college_markers)
        )
    )

    return espn_page_markers or explicit_espn


def _looks_like_gamechanger_minimal_raw_text(text: str) -> bool:
    return (
        "all plays" in text
        and (
            re.search(r"\bball\s+\d\b", text)
            or re.search(r"\bstrike\s+\d\b", text)
            or "in play." in text
            or re.search(r"\btop\s+\d+(st|nd|rd|th)\b", text)
            or re.search(r"\bbottom\s+\d+(st|nd|rd|th)\b", text)
        )
    )


def detect_source(raw_text: str) -> SourceType:
    text = raw_text.lower()

    # Cleaned GameChanger blocks remain explicit and safe.
    if _looks_like_gamechanger_cleaned_blocks(text):
        return SourceType.GAMECHANGER

    # Cleaned MLB blocks.
    if _looks_like_mlb_cleaned_blocks(text):
        return SourceType.MLB

    # ESPN full-page text must be detected before the broad
    # minimal-GameChanger rule. ESPN pages may contain "All Plays"
    # plus unrelated scoreboard text such as "Top 8th".
    if _looks_like_espn_college_raw_text(text):
        return SourceType.COLLEGE

    # Minimal GameChanger raw text.
    if _looks_like_gamechanger_minimal_raw_text(text):
        return SourceType.GAMECHANGER

    # GameChanger raw text.
    if (
        "gamechanger" in text
        or "gc.com" in text
        or "gc classic" in text
        or "plays by inning" in text
    ):
        return SourceType.GAMECHANGER

    # iScore.
    if (
        "iscoresports.com" in text
        or re.search(r"\(\d+\)\s+#\d+", text)
        or re.search(r"#\d+\s+[a-zA-Z'. -]+", raw_text)
    ):
        return SourceType.ISCORE

    # Additional college markers.
    if (
        "espn" in text
        or "ncaa baseball" in text
        or "college world series" in text
        or "men's college world series" in text
        or "college baseball" in text
    ):
        return SourceType.COLLEGE

    # MLB raw text.
    if (
        "mlb" in text
        or "baseball savant" in text
        or "statcast" in text
        or "gameday" in text
        or "pitching change" in text
    ):
        return SourceType.MLB

    return SourceType.UNKNOWN
