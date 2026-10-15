"""
Match play-by-play player names to roster names.

Platforms write the same player many ways:

    Lawson DeVault      roster / box score
    L. Devault          StatCrew, ESPN
    L Devault           GameChanger
    Devault, L.         StatCrew "last, first"
    DeVault,Lawson      StatCrew without a space
    DEVAULT             all-caps last name only
    #12 Lawson DeVault  iScore
    Law. DeVault        abbreviated first name

A play-by-play name matches a roster name when the last names agree
(case, accents, punctuation and Jr./III suffixes ignored) and whatever
first-name information is present fits the roster first name (same
initial, an abbreviation of it, or the full name). A name that fits
more than one roster player is left unmatched rather than guessed.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass


_SUFFIXES = {"jr", "sr", "ii", "iii", "iv", "v"}


def _fold(text: str) -> str:
    text = unicodedata.normalize("NFKD", str(text or ""))
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.replace("’", "'").lower()
    return text


def _tokens(text: str) -> list[str]:
    text = _fold(text)
    text = re.sub(r"^#\d+\s*", "", text.strip())
    text = re.sub(r"\([^)]*\)", " ", text)
    text = re.sub(r"[^a-z0-9,\s-]", "", text.replace("'", ""))
    return [token for token in re.split(r"[\s-]+", text) if token]


@dataclass(frozen=True)
class NameParts:
    first: str        # "" when the source gives no first-name information
    last: str         # all last-name tokens joined, e.g. "delacruz"
    last_tokens: tuple[str, ...]


def parse_name(name: str) -> NameParts:
    raw = _fold(name)
    raw = re.sub(r"^#\d+\s*", "", raw.strip())

    if "," in raw:
        last_part, _, first_part = raw.partition(",")
        last_tokens = [t for t in _tokens(last_part) if t not in _SUFFIXES and t != ","]
        first_tokens = [t for t in _tokens(first_part) if t not in _SUFFIXES and t != ","]
    else:
        tokens = [t.strip(",") for t in _tokens(raw)]
        tokens = [t for t in tokens if t and t not in _SUFFIXES]
        if len(tokens) <= 1:
            first_tokens, last_tokens = [], tokens
        else:
            first_tokens, last_tokens = tokens[:1], tokens[1:]

    first = first_tokens[0] if first_tokens else ""
    return NameParts(first=first, last="".join(last_tokens), last_tokens=tuple(last_tokens))


def _first_fits(given: str, roster_first: str) -> bool:
    """'' fits anything; 'l' fits 'lawson'; 'js' fits 'josh'; 'jal' fits 'jalen'."""
    if not given:
        return True
    if not roster_first:
        return False
    if given == roster_first or roster_first.startswith(given):
        return True
    if given[0] != roster_first[0]:
        return False
    # Abbreviation whose letters appear in order: "js" -> "josh".
    position = 0
    for letter in given:
        position = roster_first.find(letter, position)
        if position == -1:
            return False
        position += 1
    return True


# PrestoSports cuts play-by-play names to 12 characters
# ("M. Villanuev" for Mattew Villanueva).
_TRUNCATED_LENGTH = 12


def _last_fits(given: NameParts, roster: NameParts, truncated: bool = False) -> bool:
    if not given.last:
        return False
    if given.last == roster.last:
        return True
    if truncated and len(given.last) >= 4 and roster.last.startswith(given.last):
        return True
    # "Cruz" vs roster "De La Cruz"; "De La Cruz" vs roster "Cruz".
    return given.last_tokens[-1:] == roster.last_tokens[-1:] and (
        len(given.last_tokens) == 1 or len(roster.last_tokens) == 1
    )


class RosterMatcher:
    def __init__(self, roster_names) -> None:
        self.roster = [str(name).strip() for name in roster_names if str(name or "").strip()]
        self._parts = [(name, parse_name(name)) for name in self.roster]
        self._exact = {}
        for name in self.roster:
            self._exact.setdefault(" ".join(_tokens(name)), []).append(name)

    def match(self, name: str | None) -> str | None:
        if not name:
            return None

        exact = self._exact.get(" ".join(_tokens(name)))
        if exact and len(exact) == 1:
            return exact[0]

        given = parse_name(name)
        truncated = len(str(name).strip()) == _TRUNCATED_LENGTH
        candidates = [
            roster_name
            for roster_name, parts in self._parts
            if _last_fits(given, parts, truncated) and _first_fits(given.first, parts.first)
        ]

        if len(candidates) == 1:
            return candidates[0]

        # A one-token name ("Devault") may also be a first-name-only
        # roster entry; try the token as a last name only when unique.
        return None


def resolve_player_stats(
    game_players: dict[str, dict[str, int]],
    roster_names,
) -> tuple[dict[str, dict[str, int]], list[str]]:
    """
    Re-key per-player stats to roster names.

    Several play-by-play spellings of one player ("L. Devault",
    "Devault, L.") are summed into that roster player. GP is a
    per-game flag, so it is merged with max. Returns the resolved
    stats and the play-by-play names that matched no roster player.
    """

    matcher = RosterMatcher(roster_names)
    resolved: dict[str, dict[str, int]] = {}
    unmatched: list[str] = []

    for pbp_name, stats in game_players.items():
        roster_name = matcher.match(pbp_name)

        if roster_name is None:
            unmatched.append(pbp_name)
            continue

        target = resolved.setdefault(roster_name, {})
        for key, value in stats.items():
            if key == "GP":
                target[key] = max(int(target.get(key, 0)), int(value or 0))
            else:
                target[key] = int(target.get(key, 0)) + int(value or 0)

    return resolved, unmatched


__all__ = [
    "RosterMatcher",
    "parse_name",
    "resolve_player_stats",
]
