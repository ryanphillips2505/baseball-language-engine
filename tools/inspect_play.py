import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from aggregators.game_stat_aggregator import aggregate_game_stats
from assemblers.pitch_decision_builder import build_pitch_decisions
from assemblers.plate_appearance_builder import build_plate_appearance
from extractors.pitch_token_extractor import extract_pitch_tokens
from models.game import Game


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


@dataclass
class PlayInspection:
    raw_play: str
    lines: list[str]
    result_line: str
    plate_appearance: Any
    pitch_tokens: list[Any]
    pitch_decisions: list[Any]
    stat_changes: dict[str, int]


@dataclass
class GameInspection:
    raw_plays: list[str]
    play_inspections: list[PlayInspection]
    game: Game
    game_stats: dict[str, dict[str, Any]]


def _section(title: str) -> None:
    print(f"\n{title}")
    print("-" * 40)


def _subsection(title: str) -> None:
    print(f"\n{title}")
    print("=" * 40)


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


def build_play_inspection(raw_play: str) -> PlayInspection:
    lines = _clean_lines(raw_play)
    result_line = _get_result_line(raw_play, lines)

    pa = build_plate_appearance(result_line)

    pitch_tokens = extract_pitch_tokens(lines)
    pitch_decisions = build_pitch_decisions(pitch_tokens)
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

    return GameInspection(
        raw_plays=raw_plays,
        play_inspections=play_inspections,
        game=game,
        game_stats=game_stats,
    )


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
        shown_stats = []

        for key in STAT_DISPLAY_ORDER:
            value = int(player_stats.get(key, 0) or 0)

            if value:
                shown_stats.append(f"{key}={value}")

        if shown_stats:
            print(f"{player}: " + ", ".join(shown_stats))
        else:
            print(f"{player}: No tracked stats")


def print_game_inspection(inspection: GameInspection) -> None:
    _subsection("GAME WORKBENCH")

    print(f"Total raw plays: {len(inspection.raw_plays)}")
    print(f"Total plate appearances: {len(inspection.game.plate_appearances)}")

    for index, play_inspection in enumerate(inspection.play_inspections, start=1):
        _subsection(f"PLAY {index}")
        print_play_inspection(play_inspection)

    print_game_stat_summary(inspection.game_stats)


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