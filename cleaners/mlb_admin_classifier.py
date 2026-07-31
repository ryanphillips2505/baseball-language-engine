from __future__ import annotations

import re


# Challenge wrappers that embed the final baseball call are plays, not admin.
_CHALLENGE_FINAL_CALL_RE = re.compile(
    r"challenged\s*\([^)]*\)\s*,\s*call on the field was "
    r"(?:overturned|confirmed|upheld):",
    re.I,
)

_ADMIN_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"^Pitching Change:", re.I), "pitching_change"),
    (re.compile(r"^Pitching Substitution$", re.I), "pitching_change"),
    (
        re.compile(r"^Defensive Substitution:", re.I),
        "defensive_substitution",
    ),
    (re.compile(r"^Defensive Sub$", re.I), "defensive_substitution"),
    (re.compile(r"^Defensive switch\b", re.I), "defensive_switch"),
    (re.compile(r"^Defensive Switch$", re.I), "defensive_switch"),
    (
        re.compile(r"^Offensive Substitution:", re.I),
        "offensive_substitution",
    ),
    (re.compile(r"^Offensive Substitution$", re.I), "offensive_substitution"),
    (
        re.compile(r"\bremains in the game as\b", re.I),
        "defensive_assignment",
    ),
    (
        re.compile(
            r"^(Ball|Strike)\s+\d+\s+(overturned|confirmed)\s+after ABS\b",
            re.I,
        ),
        "abs_review",
    ),
    (re.compile(r"^ABS Challenge$", re.I), "abs_challenge"),
    (re.compile(r"^Challenging Team$", re.I), "abs_challenge"),
    (re.compile(r"^Injury Delay\b", re.I), "injury_delay"),
    (re.compile(r"^Game Advisory$", re.I), "game_advisory"),
    (re.compile(r"^Status Change\b", re.I), "game_advisory"),
    (re.compile(r"^Batter Timeout\b", re.I), "batter_timeout"),
    (re.compile(r"^Mound Visit\b", re.I), "mound_visit"),
    (re.compile(r"^Pitcher Step Off\b", re.I), "pitcher_step_off"),
    (re.compile(r"^Pickoff Attempt\b", re.I), "pickoff_attempt"),
    (re.compile(r"^Ejection$", re.I), "ejection"),
    (re.compile(r"\bejected by\b", re.I), "ejection"),
]


def classify_mlb_admin_line(line: str) -> str | None:
    """
    Classify MLB Gameday administrative / substitution lines.

    Returns a stable event_type string for quarantine, or None when the line
    should be handled by normal play cleaning.
    """

    text = " ".join(str(line or "").split()).strip()
    if not text:
        return None

    if _CHALLENGE_FINAL_CALL_RE.search(text):
        return None

    for pattern, event_type in _ADMIN_PATTERNS:
        if pattern.search(text):
            return event_type

    return None


__all__ = [
    "classify_mlb_admin_line",
]
