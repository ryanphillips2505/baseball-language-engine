import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from aggregators.game_stat_aggregator import aggregate_game_stats
from aggregators.swing_decision_aggregator import aggregate_swing_decisions
from assemblers.pitch_decision_builder import build_pitch_decisions
from assemblers.plate_appearance_builder import build_plate_appearance
from extractors.pitch_token_extractor import extract_pitch_tokens
from models.game import Game
from translators.damage_dataframe_builder import build_damage_dataframe
from translators.player_card_translator import build_player_cards
from translators.season_summary_translator import build_season_summary_rows
from translators.spray_zone_translator import build_spray_zone_rows
from translators.swing_decision_translator import build_swing_decision_rows
from tools.inspection.constants import STAT_DISPLAY_ORDER
from tools.inspection.models import GameInspection, PlayInspection, ReportInspection
from tools.inspection.printers import section as _section
from tools.inspection.printers import subsection as _subsection


STAT_DISPLAY_ORDER = [
    "GP",
    "K",
    "BB",
    "HBP",
    "2B",
    "3B",
    "HR",
    "XBH",
    "SB",
    "CS",
    "BIP",
    "GB",
    "FB",
    "BUNT",
    "LOC_LF",
    "LOC_CF",
    "LOC_RF",
    "LOC_3B",
    "LOC_SS",
    "LOC_2B",
    "LOC_1B",
    "LOC_P",
    "LOC_C",
    "XBH_LF",
    "XBH_CF",
    "XBH_RF",
    "XBH_UNKNOWN",
]


def _clean_lines(raw_play: str) -> list[str]:
    return [
        line.strip()
        for line in raw_play.splitlines()
        if line.strip()
    ]


def _get_result_line(raw_play: str, lines: list[str]) -> str:
    return lines[-1] if lines else raw_play.strip()


def _build_stat_changes(pa: Any) -> dict[str, int]:
    game = Game(plate_appearances=[pa])
    stats = aggregate_game_stats(game)

    player = pa.batter_name

    if not player or player not in stats:
        return {}

    player_stats = stats[player]
    changes: dict[str, int] = {}

    for key in STAT_DISPLAY_ORDER:
        value = int(player_stats.get(key, 0) or 0)

        if key == "GP":
            continue

        if value:
            changes[key] = value

    return changes


def _build_opponent_iq_stats(
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
                combo_key = (
                    key.replace("-LOC_", "-", 1)
                )
                combos[combo_key] = safe_value
            else:
                hitting[key] = safe_value

        opponent_iq_stats[player] = {
            "hitting": hitting,
            "locations": locations,
            "combos": combos,
        }

    return opponent_iq_stats


def build_play_inspection(raw_play: str) -> PlayInspection:
    lines = _clean_lines(raw_play)
    result_line = _get_result_line(raw_play, lines)

    pa = build_plate_appearance(result_line)

    pitch_tokens = extract_pitch_tokens(lines)
    pitch_decisions = build_pitch_decisions(pitch_tokens)

    pa.pitches = pitch_decisions

    stat_changes = _build_stat_changes(pa)

    return PlayInspection(
        raw_play=raw_play,
        lines=lines,
        result_line=result_line,
        plate_appearance=pa,
        pitch_tokens=pitch_tokens,
        pitch_decisions=pitch_decisions,
        stat_changes=stat_changes,
    )


def build_report_inspection(
    game_stats: dict[str, dict[str, Any]],
    swing_stats: dict[str, dict[str, dict[str, int]]],
) -> ReportInspection:
    opponent_iq_stats = _build_opponent_iq_stats(game_stats)

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


def _print_rows(rows: list[dict[str, Any]], limit: int | None = None) -> None:
    if not rows:
        print("No rows found.")
        return

    visible_rows = rows[:limit] if limit else rows

    for row in visible_rows:
        print(row)

    if limit and len(rows) > limit:
        print(f"... {len(rows) - limit} more rows")


def print_play_inspection(inspection: PlayInspection) -> None:
    pa = inspection.plate_appearance

    _section("RAW")
    print(inspection.raw_play)

    _section("CLEANED LINES")
    if inspection.lines:
        for line in inspection.lines:
            print(line)
    else:
        print("No cleaned lines found.")

    _section("RESULT LINE")
    print(inspection.result_line)

    _section("BATTER")
    print(pa.batter_name)

    _section("EVENT")
    print(pa.baseball_event)

    _section("BALL TYPE")
    print(pa.ball_type)

    _section("LOCATION")
    print(pa.location)

    _section("RUNNER EVENTS")
    if pa.runner_events:
        for runner_event in pa.runner_events:
            print(runner_event)
    else:
        print("No runner events found.")

    _section("PITCH TOKENS")
    if inspection.pitch_tokens:
        for token in inspection.pitch_tokens:
            print(token)
    else:
        print("No pitch tokens found.")

    _section("PITCH DECISIONS")
    if inspection.pitch_decisions:
        for decision in inspection.pitch_decisions:
            print(decision)
    else:
        print("No pitch decisions found.")

    _section("OPPONENT IQ STAT CHANGES")
    if inspection.stat_changes:
        for key in STAT_DISPLAY_ORDER:
            if key in inspection.stat_changes:
                print(f"{key} +{inspection.stat_changes[key]}")
    else:
        print("No tracked Opponent IQ stat changes.")


def print_game_stat_summary(game_stats: dict[str, dict[str, Any]]) -> None:
    _section("COMBINED GAME STATS")

    if not game_stats:
        print("No game stats found.")
        return

    for player in sorted(game_stats):
        player_stats = game_stats[player]
        print(player_stats)
        shown_stats = []

        for key in STAT_DISPLAY_ORDER:
            value = int(player_stats.get(key, 0) or 0)

            if value:
                shown_stats.append(f"{key}={value}")

        if shown_stats:
            print(f"{player}: " + ", ".join(shown_stats))
        else:
            print(f"{player}: No tracked stats")


def print_swing_stat_summary(
    swing_stats: dict[str, dict[str, dict[str, int]]],
) -> None:
    _section("COMBINED SWING DECISION STATS")

    if not swing_stats:
        print("No swing decision stats found.")
        return

    for player in sorted(swing_stats):
        print(f"{player}:")
        player_counts = swing_stats[player]

        for count, bucket in player_counts.items():
            pa = int(bucket.get("PA", 0) or 0)

            if not pa:
                continue

            print(
                f"  {count}: "
                f"PA={bucket.get('PA', 0)}, "
                f"BIP={bucket.get('BIP', 0)}, "
                f"SWING_MISS={bucket.get('SWING_MISS', 0)}, "
                f"FOUL={bucket.get('FOUL', 0)}, "
                f"CALLED_STRIKE={bucket.get('CALLED_STRIKE', 0)}, "
                f"BALL={bucket.get('BALL', 0)}"
            )


def print_report_inspection(reports: ReportInspection) -> None:
    _subsection("REPORT WORKBENCH")

    _section("SEASON SUMMARY ROWS")
    _print_rows(reports.season_summary_rows)

    _section("SPRAY ZONE ROWS")
    _print_rows(reports.spray_zone_rows)

    _section("DAMAGE ROWS")
    _print_rows(reports.damage_rows)

    _section("SWING DECISION ROWS")
    _print_rows(reports.swing_decision_rows, limit=20)

    _section("PLAYER CARDS")
    _print_rows(reports.player_cards)


def print_game_inspection(inspection: GameInspection) -> None:
    _subsection("GAME WORKBENCH")

    print(f"Total raw plays: {len(inspection.raw_plays)}")
    print(f"Total plate appearances: {len(inspection.game.plate_appearances)}")

    for index, play_inspection in enumerate(inspection.play_inspections, start=1):
        _subsection(f"PLAY {index}")
        print_play_inspection(play_inspection)

    print_game_stat_summary(inspection.game_stats)
    print_swing_stat_summary(inspection.swing_stats)
    print_report_inspection(inspection.reports)


def inspect_play(raw_play: str) -> None:
    inspection = build_play_inspection(raw_play)
    print_play_inspection(inspection)


def inspect_game(raw_plays: list[str]) -> None:
    inspection = build_game_inspection(raw_plays)
    print_game_inspection(inspection)


if __name__ == "__main__":
    inspect_game(
        [
            "Ball 1, Strike 1 looking, Foul, In play.\n"
            "Wade Webb doubles on a fly ball to center field.",
            "Strike 1 swinging, Strike 2 looking, Strike 3 swinging.\n"
            "John Smith strikes out swinging.",
            "Ball 1, Ball 2, Ball 3, Ball 4.\n"
            "Trey Jones walks.",
        ]
    )