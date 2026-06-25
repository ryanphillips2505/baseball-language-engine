import sys
from pathlib import Path

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


def _section(title: str) -> None:
    print(f"\n{title}")
    print("-" * 40)


def _print_stat_changes(pa) -> None:
    game = Game(plate_appearances=[pa])
    stats = aggregate_game_stats(game)

    player = pa.batter_name

    if not player or player not in stats:
        print("No batter stat changes found.")
        return

    player_stats = stats[player]

    found = False

    for key in STAT_DISPLAY_ORDER:
        value = int(player_stats.get(key, 0) or 0)

        if key == "GP":
            continue

        if value:
            print(f"{key} +{value}")
            found = True

    if not found:
        print("No tracked Opponent IQ stat changes.")


def inspect_play(raw_play: str) -> None:
    _section("RAW")
    print(raw_play)

    lines = [
        line.strip()
        for line in raw_play.splitlines()
        if line.strip()
    ]

    result_line = lines[-1] if lines else raw_play

    pa = build_plate_appearance(result_line)

    pitch_tokens = extract_pitch_tokens(lines)
    pitch_decisions = build_pitch_decisions(pitch_tokens)

    _section("RESULT LINE")
    print(result_line)

    _section("BATTER")
    print(pa.batter_name)

    _section("EVENT")
    print(pa.baseball_event)

    _section("BALL TYPE")
    print(pa.ball_type)

    _section("LOCATION")
    print(pa.location)

    _section("RUNNER EVENTS")
    print(pa.runner_events)

    _section("PITCH TOKENS")
    print(pitch_tokens)

    _section("PITCH DECISIONS")
    if pitch_decisions:
        for decision in pitch_decisions:
            print(decision)
    else:
        print("No pitch decisions found.")

    _section("OPPONENT IQ STAT CHANGES")
    _print_stat_changes(pa)


if __name__ == "__main__":
    inspect_play(
        "Ball 1, Strike 1 looking, Foul, In play.\n"
        "Wade Webb doubles on a fly ball to center field."
    )