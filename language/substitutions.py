"""
Pinch-runner and courtesy-runner entries, in each platform's wording.

Opponent IQ credits PR / CR to the runner who enters the game (Legacy
definition). Substitution lines are not plays, so cleaners drop them;
this reads them from the raw text instead.

    GameChanger style  Lineup changed: Pinch runner Jake Lee in for catcher Bo Hart
                       Courtesy runner Jake Lee in for Bo Hart
    StatCrew / ESPN    Lee pinch ran for Hart.   /   J. Lee ran for B. Hart.
                       Lee courtesy ran for Hart.
    MLB Gameday        Offensive Substitution: Pinch-runner Jake Lee replaces Bo Hart.
"""

from __future__ import annotations

import re


_RULES: list[tuple[re.Pattern, str]] = [
    (re.compile(r"Pinch runner\s+(?P<name>.+?)\s+in\s+for\b", re.I), "PR"),
    (re.compile(r"Courtesy runner\s+(?P<name>.+?)\s+in\s+for\b", re.I), "CR"),
    (re.compile(r"Pinch-runner\s+(?P<name>.+?)\s+replaces\b", re.I), "PR"),
    (re.compile(r"^(?P<name>[^;:]+?)\s+courtesy[- ]?(?:ran|running|runner)\s+for\b", re.I), "CR"),
    (re.compile(r"^(?P<name>[^;:]+?)\s+pinch[- ]?(?:ran|running|runner)\s+for\b", re.I), "PR"),
    # ESPN generated: "J. Lee ran for B. Hart."
    (re.compile(r"^(?P<name>(?:[A-Z][\w'.\-]*\.?\s+){0,3}[A-Z][\w'.\-]*)\s+ran for\b"), "PR"),
]


def extract_runner_entries(raw_text: str) -> list[tuple[str, str]]:
    """Return (runner name, "PR" or "CR") for each runner substitution line."""
    entries: list[tuple[str, str]] = []

    for raw_line in str(raw_text or "").splitlines():
        line = " ".join(raw_line.split()).strip()
        if not line:
            continue

        for pattern, key in _RULES:
            match = pattern.search(line)
            if match:
                name = match.group("name").strip(" ,;:")
                if name:
                    entries.append((name, key))
                break

    return entries


__all__ = [
    "extract_runner_entries",
]
