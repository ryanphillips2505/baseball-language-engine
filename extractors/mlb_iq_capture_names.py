from __future__ import annotations

import re

from extractors.mlb_boxscore_name_mapper import (
    map_box_tokens_to_full_names,
    parse_box_player_token,
)
from extractors.player_extractor import extract_batter_name
from pipeline.process_game import process_game


_SUB_NAME_RE = re.compile(
    r"(?:Pinch-hitter|Pinch-runner|Defensive Substitution:|Pitching Change:)\s+"
    r"([A-Z][A-Za-zÀ-ÿ'’. -]+?)(?:\s+replaces\b|\s+replaces,|\s*$)",
    re.I,
)

_REMAINS_NAME_RE = re.compile(
    r"^([A-Z][A-Za-zÀ-ÿ'’. -]+?)\s+remains in the game as\b",
    re.I,
)


def extract_box_player_tokens(raw_text: str) -> list[str]:
    """
    Pull glued box-score identity tokens from an MLB.com IQ Capture paste.

    Stops at batting notes / pitching sections so HR lines like
    "HRRafaela (...)" are not treated as player rows.
    """

    tokens: list[str] = []
    seen: set[str] = set()

    for raw_line in raw_text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        upper = line.upper()
        if upper.startswith("BATTING") or upper.startswith("FIELDING"):
            # Finished a batter table; keep scanning for the other club.
            continue
        if upper.startswith("PITCHES-STRIKES") or upper.startswith("UMPIRES"):
            break
        if line.startswith("HR") and "(" in line:
            continue
        if line.startswith("TB") or line.startswith("RBI") or line.startswith("DP"):
            continue

        ref = parse_box_player_token(line)
        if ref is None:
            continue
        if line in seen:
            continue
        seen.add(line)
        tokens.append(line)

    return tokens


def extract_full_player_names(raw_text: str) -> list[str]:
    """Collect full names from PAs plus substitution / defensive lines."""

    names: list[str] = []
    seen: set[str] = set()

    def _add(name: str | None) -> None:
        if not name:
            return
        cleaned = " ".join(name.split()).strip(" .")
        if not cleaned or cleaned in seen:
            return
        seen.add(cleaned)
        names.append(cleaned)

    game = process_game(raw_text)
    for pa in game.plate_appearances:
        _add(pa.batter_name)
        # Also harvest names embedded in play text via batter extractor only;
        # runner/fielder identity can wait for a later slice.

    for line in raw_text.splitlines():
        text = " ".join(line.split()).strip()
        if not text:
            continue
        for match in _SUB_NAME_RE.finditer(text):
            _add(match.group(1))
        remains = _REMAINS_NAME_RE.match(text)
        if remains:
            _add(remains.group(1))
        # Play lines themselves:
        if extract_batter_name(text):
            _add(extract_batter_name(text))

    return names


def build_box_to_pbp_name_map(raw_text: str) -> dict[str, str]:
    """Map IQ Capture box tokens -> full play-by-play names for one paste."""

    return map_box_tokens_to_full_names(
        extract_box_player_tokens(raw_text),
        extract_full_player_names(raw_text),
    )


__all__ = [
    "extract_box_player_tokens",
    "extract_full_player_names",
    "build_box_to_pbp_name_map",
]
