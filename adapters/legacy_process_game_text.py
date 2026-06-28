from __future__ import annotations

import re

from adapters.opponent_iq_adapter import adapt_game_stats_to_opponent_iq
from aggregators.game_stat_aggregator import aggregate_game_stats
from pipeline.process_game import process_game


_SUFFIX_PATTERN = re.compile(r"\b(Jr\.?|Sr\.?|II|III|IV)\b", re.IGNORECASE)


def _normalize_player_name(name: str) -> str:
    if not name:
        return ""

    name = str(name)
    name = name.replace("’", "'")
    name = re.sub(r"\s*\([^()]*\)", "", name)
    name = _SUFFIX_PATTERN.sub("", name)
    name = re.sub(r"[^A-Za-z0-9\s]", "", name)
    name = " ".join(name.split())

    return name.lower().strip()


def _filter_players_by_roster(
    game_players: dict[str, dict[str, int]],
    roster_names: set[str] | None,
) -> dict[str, dict[str, int]]:
    if not roster_names:
        return game_players

    roster_map = {
        _normalize_player_name(name): str(name).strip()
        for name in roster_names
        if _normalize_player_name(name)
    }

    filtered: dict[str, dict[str, int]] = {}

    for player_name, stats in game_players.items():
        normalized = _normalize_player_name(player_name)

        if normalized in roster_map:
            filtered[roster_map[normalized]] = stats

    return filtered


def process_game_text(
    raw_text: str,
    roster_names: set[str] | None = None,
) -> tuple[dict, dict]:
    """
    Compatibility adapter.

    Returns the same (game_team, game_players) structure that the
    legacy Opponent IQ parser returns today, but generated entirely
    by the Baseball Language Engine.
    """

    game = process_game(raw_text)

    game_stats = aggregate_game_stats(game)

    game_players = adapt_game_stats_to_opponent_iq(game_stats)

    game_players = _filter_players_by_roster(
        game_players,
        roster_names,
    )

    game_team: dict[str, int] = {}

    for player_stats in game_players.values():
        for key, value in player_stats.items():
            if key == "GP":
                continue

            game_team[key] = game_team.get(key, 0) + int(value)

    all_game_players = adapt_game_stats_to_opponent_iq(game_stats)

    game_team["SB"] = sum(
        int(player_stats.get("SB", 0))
        for player_stats in all_game_players.values()
    )

    game_team["CS"] = sum(
        int(player_stats.get("CS", 0))
        for player_stats in all_game_players.values()
    )

    return game_team, game_players


__all__ = [
    "process_game_text",
]