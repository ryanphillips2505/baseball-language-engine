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

    # -------------------------
    # CLEANED GAMECHANGER BLOCKS
    # -------------------------
    if _looks_like_gamechanger_cleaned_blocks(text):
        return SourceType.GAMECHANGER

    # -------------------------
    # CLEANED MLB BLOCKS
    # -------------------------
    if _looks_like_mlb_cleaned_blocks(text):
        return SourceType.MLB

    # -------------------------
    # MINIMAL GAMECHANGER RAW TEXT
    # -------------------------
    if _looks_like_gamechanger_minimal_raw_text(text):
        return SourceType.GAMECHANGER

    # -------------------------
    # GAMECHANGER RAW TEXT
    # -------------------------
    if (
        "gamechanger" in text
        or "gc.com" in text
        or "gc classic" in text
        or "plays by inning" in text
    ):
        return SourceType.GAMECHANGER

    # -------------------------
    # ISCORE
    # -------------------------
    if (
        "iscoresports.com" in text
        or re.search(r"\(\d+\)\s+#\d+", text)
        or re.search(r"#\d+\s+[a-zA-Z'. -]+", raw_text)
    ):
        return SourceType.ISCORE

    # -------------------------
    # ESPN / COLLEGE
    # -------------------------
    if (
        "espn" in text
        or "ncaa baseball" in text
        or "college world series" in text
        or "men's college world series" in text
        or "college baseball" in text
    ):
        return SourceType.COLLEGE

    # -------------------------
    # MLB RAW TEXT
    # -------------------------
    if (
        "mlb" in text
        or "baseball savant" in text
        or "statcast" in text
        or "gameday" in text
        or "pitching change" in text
    ):
        return SourceType.MLB

    return SourceType.UNKNOWN