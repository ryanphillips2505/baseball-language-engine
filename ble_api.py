from __future__ import annotations

from dataclasses import dataclass

from aggregators.game_stat_aggregator import aggregate_game_stats
from aggregators.swing_decision_aggregator import aggregate_swing_decisions
from pipeline.process_game import process_game
from translators.damage_dataframe_builder import build_damage_dataframe
from translators.player_card_translator import build_player_cards
from translators.season_summary_dataframe_builder import (
    build_season_summary_dataframe,
)
from translators.spray_zone_dataframe_builder import (
    build_spray_zone_dataframe,
)
from translators.swing_decision_dataframe_builder import (
    build_swing_decision_dataframe,
)


@dataclass(slots=True)
class BLEOutput:
    game: object
    game_stats: dict
    swing_stats: dict
    season_summary: list
    spray_zone: list
    damage: list
    swing_decisions: list
    player_cards: list


def build(raw_text: str) -> BLEOutput:

    game = process_game(raw_text)

    game_stats = aggregate_game_stats(game)
    swing_stats = aggregate_swing_decisions(game)

    return BLEOutput(
        game=game,
        game_stats=game_stats,
        swing_stats=swing_stats,
        season_summary=build_season_summary_dataframe(game_stats),
        spray_zone=build_spray_zone_dataframe(game_stats),
        damage=build_damage_dataframe(game_stats),
        swing_decisions=build_swing_decision_dataframe(swing_stats),
        player_cards=build_player_cards(game_stats, swing_stats),
    )
