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


def _section(title: str) -> None:
    print(f"\n{title}")
    print("-" * 40)


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


def inspect_play(raw_play: str) -> None:
    inspection = build_play_inspection(raw_play)
    print_play_inspection(inspection)


if __name__ == "__main__":
    inspect_play(
        "Ball 1, Strike 1 looking, Foul, In play.\n"
        "Wade Webb doubles on a fly ball to center field."
    )