from typing import Any

from aggregators.game_stat_aggregator import aggregate_game_stats
from aggregators.swing_decision_aggregator import aggregate_swing_decisions
from models.game import Game

from .models import GameInspection
from .play_inspector import build_play_inspection
from .report_inspector import build_report_inspection


def build_game_inspection(raw_plays: list[str]) -> GameInspection:
    play_inspections = [
        build_play_inspection(raw_play)
        for raw_play in raw_plays
    ]

    game = Game(
        plate_appearances=[
            inspection.plate_appearance
            for inspection in play_inspections
        ]
    )

    game_stats = aggregate_game_stats(game)
    swing_stats = aggregate_swing_decisions(game)
    reports = build_report_inspection(game_stats, swing_stats)

    return GameInspection(
        raw_plays=raw_plays,
        play_inspections=play_inspections,
        game=game,
        game_stats=game_stats,
        swing_stats=swing_stats,
        reports=reports,
    )