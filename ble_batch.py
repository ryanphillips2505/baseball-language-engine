from __future__ import annotations

from pathlib import Path

from aggregators.game_stat_aggregator import aggregate_game_stats
from pipeline.process_game import process_game


def process_directory(directory: str) -> dict[str, dict]:

    season_stats: dict[str, dict] = {}

    for file in sorted(Path(directory).glob("*.txt")):

        raw_text = file.read_text(encoding="utf-8")

        game = process_game(raw_text)

        game_stats = aggregate_game_stats(game)

        for player, stats in game_stats.items():

            if player not in season_stats:
                season_stats[player] = {}

            for stat, value in stats.items():
                season_stats[player][stat] = (
                    season_stats[player].get(stat, 0)
                    + value
                )

    return season_stats
