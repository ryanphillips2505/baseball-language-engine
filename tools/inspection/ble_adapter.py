from __future__ import annotations

from aggregators.game_stat_aggregator import aggregate_game_stats
from pipeline.process_game import process_game


def build_ble_stats(raw_text: str) -> dict:

    game = process_game(raw_text)

    return aggregate_game_stats(game)
