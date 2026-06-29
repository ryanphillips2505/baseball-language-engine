from __future__ import annotations

from aggregators.game_stat_aggregator import aggregate_game_stats
from pipeline.process_game import process_game


def parse(raw_text: str):
    """
    Parse raw play-by-play into a Game model.
    """
    return process_game(raw_text)


def stats(raw_text: str):
    """
    Parse raw play-by-play and return Opponent IQ stats.
    """
    game = process_game(raw_text)
    return aggregate_game_stats(game)
