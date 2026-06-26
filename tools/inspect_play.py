import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.inspection.workbench import Workbench


def inspect_play(raw_play: str) -> None:
    workbench = Workbench()
    inspection = workbench.inspect_play(raw_play)
    workbench.print_play(inspection)


def inspect_game(raw_plays: list[str]) -> None:
    workbench = Workbench()
    inspection = workbench.inspect_game(raw_plays)
    workbench.print_game(inspection)


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