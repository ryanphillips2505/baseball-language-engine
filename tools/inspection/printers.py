from typing import Any

from .constants import STAT_DISPLAY_ORDER
from .models import GameInspection, PlayInspection, ReportInspection


def section(title: str) -> None:
    print(f"\n{title}")
    print("-" * 40)


def subsection(title: str) -> None:
    print(f"\n{title}")
    print("=" * 40)


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

    section("RAW")
    print(inspection.raw_play)

    section("CLEANED LINES")
    if inspection.lines:
        for line in inspection.lines:
            print(line)
    else:
        print("No cleaned lines found.")

    section("RESULT LINE")
    print(inspection.result_line)

    section("BATTER")
    print(pa.batter_name)

    section("EVENT")
    print(pa.baseball_event)

    section("BALL TYPE")
    print(pa.ball_type)

    section("LOCATION")
    print(pa.location)

    section("RUNNER EVENTS")
    if pa.runner_events:
        for runner_event in pa.runner_events:
            print(runner_event)
    else:
        print("No runner events found.")

    section("PITCH TOKENS")
    if inspection.pitch_tokens:
        for token in inspection.pitch_tokens:
            print(token)
    else:
        print("No pitch tokens found.")

    section("PITCH DECISIONS")
    if inspection.pitch_decisions:
        for decision in inspection.pitch_decisions:
            print(decision)
    else:
        print("No pitch decisions found.")

    section("OPPONENT IQ STAT CHANGES")
    if inspection.stat_changes:
        for key in STAT_DISPLAY_ORDER:
            if key in inspection.stat_changes:
                print(f"{key} +{inspection.stat_changes[key]}")
    else:
        print("No tracked Opponent IQ stat changes.")


def print_game_stat_summary(game_stats: dict[str, dict[str, Any]]) -> None:
    section("COMBINED GAME STATS")

    if not game_stats:
        print("No game stats found.")
        return

    for player in sorted(game_stats):
        player_stats = game_stats[player]
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
    section("COMBINED SWING DECISION STATS")

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
    subsection("REPORT WORKBENCH")

    section("SEASON SUMMARY ROWS")
    _print_rows(reports.season_summary_rows)

    section("SPRAY ZONE ROWS")
    _print_rows(reports.spray_zone_rows)

    section("DAMAGE ROWS")
    _print_rows(reports.damage_rows)

    section("SWING DECISION ROWS")
    _print_rows(reports.swing_decision_rows, limit=20)

    section("PLAYER CARDS")
    _print_rows(reports.player_cards)


def print_game_inspection(inspection: GameInspection) -> None:
    subsection("GAME WORKBENCH")

    print(f"Total raw plays: {len(inspection.raw_plays)}")
    print(f"Total plate appearances: {len(inspection.game.plate_appearances)}")

    for index, play_inspection in enumerate(inspection.play_inspections, start=1):
        subsection(f"PLAY {index}")
        print_play_inspection(play_inspection)

    print_game_stat_summary(inspection.game_stats)
    print_swing_stat_summary(inspection.swing_stats)
    print_report_inspection(inspection.reports)