from __future__ import annotations

from adapters.opponent_iq_adapter import adapt_game_stats_to_opponent_iq
from aggregators.game_stat_aggregator import aggregate_game_stats
from pipeline.process_game import process_game


def process_game_text(raw_text: str) -> tuple[dict, dict]:
    """
    Compatibility adapter.

    Returns the same (game_team, game_players) structure that the
    legacy Opponent IQ parser returns today, but generated entirely
    by the Baseball Language Engine.
    """

    game = process_game(raw_text)

    game_stats = aggregate_game_stats(game)

    game_players = adapt_game_stats_to_opponent_iq(game_stats)

    game_team: dict[str, int] = {}

    for player_stats in game_players.values():
        for key, value in player_stats.items():
            game_team[key] = game_team.get(key, 0) + int(value)

    return game_team, game_players


__all__ = [
    "process_game_text",
]