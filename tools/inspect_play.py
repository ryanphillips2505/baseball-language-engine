import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.inspection.game_inspector import build_game_inspection
from tools.inspection.play_inspector import build_play_inspection
from tools.inspection.printers import print_game_inspection, print_play_inspection


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