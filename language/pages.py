"""
Whole college box-score pages (SIDEARM, PrestoSports) pasted as text.

These pages repeat plays:
- SIDEARM: a Scoring Summary, then "All Innings", then the same innings
  again under per-inning tabs ("Alabama - Top of 1st" ... appears twice)
- PrestoSports: the Scoring Summary twice, then "All Plays"

Reading every line would count a scoring play two or three times. The
extractor keeps only half-inning sections, and only the first copy of
each, so every play is read once. Text with fewer than two half-inning
headers (a plain play-by-play paste) is returned unchanged.

GameChanger never comes through here: GameChanger half-inning headers
read "Top 1st - Team" (no "of"), and GameChanger structure vetoes the
page recognizer.
"""

from __future__ import annotations

import re


# "Alabama - Top of 1st" / "Top of 1st" / "Top of 1st Inning" / "Top of the 3rd inning"
_HALF_HEADER_RE = re.compile(
    r"^\s*(?:(?P<team>.+?)\s*[-–—]\s*)?"
    r"(?P<half>top|bottom)\s+of\s+(?:the\s+)?(?P<inning>\d+)(?:st|nd|rd|th)?"
    r"(?:\s+inning)?\s*\|?\s*$",
    re.IGNORECASE,
)

# "2 Runs, 3 Hits, 0 Error, 1 Left on Base" / "RUNS 0 HITS 1 ERRORS 0 LEFT ON BASE 3"
_INNING_SUMMARY_RE = re.compile(
    r"^\s*(?:\d+\s+runs?,\s*\d+\s+hits?\b|runs\s+\d+\s+hits\s+\d+\b)",
    re.IGNORECASE,
)

_STATCREW_PLAY_RE = re.compile(
    r"(?im)\b(?:struck out (?:swinging|looking)|grounded out to|grounded into|"
    r"flied out to|lined out to|popped (?:up|out) to|fouled out to|"
    r"singled (?:to|through|up|down)|doubled (?:to|down)|tripled (?:to|down)|"
    r"homered (?:to|down)|walked\b|hit by pitch|reached on)"
)

# PrestoSports marks every out on its own line: "(1 out)", "( out)".
# Presto pages scored with GameChanger-style wording ("Smith grounds out
# to second baseman") carry these; GameChanger and MLB pages never do.
_PRESTO_OUT_MARKER_RE = re.compile(r"(?im)^\s*\(\s*\d?\s*outs?\)\s*$")
_MIN_OUT_MARKERS = 3

# GameChanger structure: "Top 1st - Team", pitch lines, "In play." lines.
_GC_HALF_HEADER_RE = re.compile(r"(?im)^\s*(?:top|bottom)\s+\d+(?:st|nd|rd|th)\s+-\s+\S")
_GC_PITCH_LINE_RE = re.compile(r"(?im)^\s*(?:ball|strike)\s+\d\b|\bin play\.")

_MIN_HEADERS = 2
_MIN_PLAYS = 5


def _header_key(match: re.Match) -> tuple[str, str]:
    return match.group("half").lower(), match.group("inning")


def half_inning_headers(text: str) -> int:
    return sum(1 for line in str(text or "").splitlines() if _HALF_HEADER_RE.match(line))


def has_gamechanger_structure(text: str) -> bool:
    text = str(text or "")
    return bool(_GC_HALF_HEADER_RE.search(text) or _GC_PITCH_LINE_RE.search(text))


def looks_like_statcrew_page(text: str) -> bool:
    """A whole SIDEARM / Presto style page: inning sections + StatCrew plays."""
    text = str(text or "")
    if has_gamechanger_structure(text):
        return False
    if half_inning_headers(text) < _MIN_HEADERS:
        return False
    return (
        len(_STATCREW_PLAY_RE.findall(text)) >= _MIN_PLAYS
        or len(_PRESTO_OUT_MARKER_RE.findall(text)) >= _MIN_OUT_MARKERS
    )


def extract_statcrew_plays(text: str) -> str:
    """
    Keep each half inning once, drop everything outside the innings.

    Returns the text unchanged when it is not a sectioned page.
    """
    lines = str(text or "").splitlines()

    if half_inning_headers(text) < _MIN_HEADERS:
        return str(text or "")

    kept: list[str] = []
    seen: set[tuple[str, str]] = set()
    in_section = False
    keep = False

    for line in lines:
        header = _HALF_HEADER_RE.match(line)
        if header:
            key = _header_key(header)
            in_section = True
            keep = key not in seen
            seen.add(key)
            continue

        if not in_section:
            continue

        if _INNING_SUMMARY_RE.match(line):
            in_section = False
            continue

        if keep:
            kept.append(line)

    return "\n".join(kept)


__all__ = [
    "extract_statcrew_plays",
    "has_gamechanger_structure",
    "half_inning_headers",
    "looks_like_statcrew_page",
]
