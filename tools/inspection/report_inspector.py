from typing import Any

from translators.damage_dataframe_builder import build_damage_dataframe
from translators.player_card_translator import build_player_cards
from translators.season_summary_translator import build_season_summary_rows
from translators.spray_zone_translator import build_spray_zone_rows
from translators.swing_decision_translator import build_swing_decision_rows

from .models import ReportInspection


def build_opponent_iq_stats(
    game_stats: dict[str, dict[str, Any]],
) -> dict[str, dict[str, dict[str, int]]]:
    opponent_iq_stats: dict[str, dict[str, dict[str, int]]] = {}

    for player, stats in game_stats.items():
        hitting: dict[str, int] = {}
        locations: dict[str, int] = {}
        combos: dict[str, int] = {}

        for key, value in stats.items():
            safe_value = int(value or 0)

            if key.startswith("LOC_"):
                location_key = key.replace("LOC_", "")
                locations[location_key] = safe_value

            elif key.startswith(("GB-LOC_", "FB-LOC_", "BUNT-LOC_")):
                combo_key = key.replace("-LOC_", "-", 1)
                combos[combo_key] = safe_value

            else:
                hitting[key] = safe_value

        opponent_iq_stats[player] = {
            "hitting": hitting,
            "locations": locations,
            "combos": combos,
        }

    return opponent_iq_stats


def build_report_inspection(
    game_stats: dict[str, dict[str, Any]],
    swing_stats: dict[str, dict[str, dict[str, int]]],
) -> ReportInspection:
    opponent_iq_stats = build_opponent_iq_stats(game_stats)

    season_summary_rows = build_season_summary_rows(opponent_iq_stats)
    spray_zone_rows = build_spray_zone_rows(season_summary_rows)
    damage_df = build_damage_dataframe(season_summary_rows)
    swing_decision_rows = build_swing_decision_rows(swing_stats)
    player_cards = build_player_cards(game_stats, swing_stats)

    return ReportInspection(
        season_summary_rows=season_summary_rows,
        spray_zone_rows=spray_zone_rows,
        damage_rows=damage_df.to_dict("records"),
        swing_decision_rows=swing_decision_rows,
        player_cards=player_cards,
    )