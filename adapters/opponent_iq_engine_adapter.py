from __future__ import annotations

from adapters.opponent_iq_adapter import adapt_game_stats_to_opponent_iq
from aggregators.game_stat_aggregator import aggregate_game_stats
from pipeline.process_game import process_game


def _sum_team_totals(game_players: dict[str, dict[str, int]]) -> dict[str, int]:
    team_totals: dict[str, int] = {}

    for player_stats in (game_players or {}).values():
        for key, value in (player_stats or {}).items():
            # Legacy Opponent IQ does not aggregate GP into team totals.
            # GP is player-level only.
            if key == "GP":
                continue

            team_totals[key] = team_totals.get(key, 0) + int(value or 0)

    team_totals.setdefault("GP", 0)

    return team_totals


def process_raw_text_to_opponent_iq_stats(
    raw_text: str,
) -> dict[str, dict[str, int]]:
    game = process_game(raw_text)
    game_stats = aggregate_game_stats(game)

    return adapt_game_stats_to_opponent_iq(game_stats)


def process_raw_text_to_opponent_iq_game(
    raw_text: str,
) -> tuple[dict[str, int], dict[str, dict[str, int]]]:
    game_players = process_raw_text_to_opponent_iq_stats(raw_text)
    game_team = _sum_team_totals(game_players)

    return game_team, game_players


__all__ = [
    "process_raw_text_to_opponent_iq_stats",
    "process_raw_text_to_opponent_iq_game",
]
