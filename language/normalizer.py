"""
Rewrite platform vocabulary into BLE canonical wording.

Only aliases are rewritten. A rewrite never adds information that is
not in the source text: "to ss" and "to shortstop" say the same thing,
"down the lf line" names left field, "up the middle" names center.

Position abbreviations are matched case-sensitively in lowercase so
player initials ("C. Smith", "P. Jones") are never touched.
"""

from __future__ import annotations

import re


# StatCrew-family count + pitch sequence, e.g. "(1-2 KBKS)" or "(0-0)".
PITCH_SEQUENCE_RE = re.compile(r"\((?P<count>[0-3]-[0-2])(?:\s+(?P<sequence>[A-Z]*))?\)")

_REVIEW_PREFIX_RE = re.compile(
    r"^[^:]*\b(?:challenged|review(?:ed)?|overturned|confirmed|stands)\b[^:]*:\s*",
    re.I,
)

_DIRECTION_RULES: list[tuple[re.Pattern, str]] = [
    (re.compile(r"\bdown the (?:lf|left[- ]field) line\b", re.I), "to left field"),
    (re.compile(r"\bdown the (?:rf|right[- ]field) line\b", re.I), "to right field"),
    (re.compile(r"\bdown the (?:1b|first[- ]base) line\b", re.I), "to first base"),
    (re.compile(r"\bdown the (?:3b|third[- ]base) line\b", re.I), "to third base"),
    (re.compile(r"\bup the middle\b", re.I), "to center field"),
    (re.compile(r"\bthrough the left side\b", re.I), "to left field"),
    (re.compile(r"\bthrough the right side\b", re.I), "to right field"),
    (re.compile(r"\bto (?:shallow|deep|short|medium) (left|center|right)\b", re.I), r"to \1"),
    (re.compile(r"\bto short\b(?!stop)", re.I), "to shortstop"),
    (re.compile(r"\bin (?:third|3b) base side foul territory\b", re.I), "in foul territory"),
    (re.compile(r"\bin (?:first|1b) base side foul territory\b", re.I), "in foul territory"),
]

_POSITION_ABBREVIATIONS = {
    "p": "pitcher",
    "c": "catcher",
    "1b": "first baseman",
    "2b": "second baseman",
    "3b": "third baseman",
    "ss": "shortstop",
    "lf": "left fielder",
    "cf": "center fielder",
    "rf": "right fielder",
}

# Lowercase only, standalone token. Never matches initials ("C.") or
# pitch codes (uppercase).
_POSITION_ABBREVIATION_RE = re.compile(
    r"(?<![A-Za-z0-9.'])(p|c|1b|2b|3b|ss|lf|cf|rf)(?![A-Za-z0-9]|\.[A-Za-z])"
)

_GLUED_WORD_RULES: list[tuple[re.Pattern, str]] = [
    (re.compile(r"\bcaught stealing(?=[a-z])"), "caught stealing "),
    (re.compile(r"\binside-the-park\b", re.I), "inside the park"),
    (re.compile(r"\bground rule double\b", re.I), "ground-rule double"),
]


def strip_pitch_sequence(text: str) -> str:
    return PITCH_SEQUENCE_RE.sub("", text)


def normalize_play_text(text: str) -> str:
    normalized = str(text or "").replace("’", "'").replace(" ", " ")
    normalized = re.sub(r"\s+", " ", normalized).strip()

    normalized = _REVIEW_PREFIX_RE.sub("", normalized)
    normalized = strip_pitch_sequence(normalized)

    for pattern, replacement in _GLUED_WORD_RULES:
        normalized = pattern.sub(replacement, normalized)

    for pattern, replacement in _DIRECTION_RULES:
        normalized = pattern.sub(replacement, normalized)

    normalized = _POSITION_ABBREVIATION_RE.sub(
        lambda match: _POSITION_ABBREVIATIONS[match.group(1)],
        normalized,
    )

    normalized = re.sub(r"\s+([,.;])", r"\1", normalized)
    return re.sub(r"\s+", " ", normalized).strip()


__all__ = [
    "PITCH_SEQUENCE_RE",
    "normalize_play_text",
    "strip_pitch_sequence",
]
