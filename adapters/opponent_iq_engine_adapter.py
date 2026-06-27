from __future__ import annotations

from adapters.opponent_iq_adapter import adapt_game_stats_to_opponent_iq
from aggregators.game_stat_aggregator import aggregate_game_stats
from pipeline.process_game import process_game


def process_raw_text_to_opponent_iq_stats(
    raw_text: str,
) -> dict[str, dict[str, int]]:
    game = process_game(raw_text)
    game_stats = aggregate_game_stats(game)

    return adapt_game_stats_to_opponent_iq(game_stats)


__all__ = [
    "process_raw_text_to_opponent_iq_stats",
]