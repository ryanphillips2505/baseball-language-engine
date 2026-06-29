from __future__ import annotations

import sys

from .ble_inspector import inspect_ble_file
from .game_inspector import build_game_inspection
from .game_loader import load_game_file
from .models import GameInspection, PlayInspection
from .play_inspector import build_play_inspection
from .printers import (
    print_game_inspection,
    print_play_inspection,
)


class Workbench:

    def inspect_play(self, raw_play: str) -> PlayInspection:
        return build_play_inspection(raw_play)

    def inspect_game(self, raw_plays: list[str]) -> GameInspection:
        return build_game_inspection(raw_plays)

    def print_play(self, inspection: PlayInspection) -> None:
        print_play_inspection(inspection)

    def print_game(self, inspection: GameInspection) -> None:
        print_game_inspection(inspection)

    def inspect_game_file(self, path: str):
        raw_plays = load_game_file(path)
        return self.inspect_game(raw_plays)

    def inspect_ble_file(self, path: str):
        return inspect_ble_file(path)

    def print_ble_file_inspection(self, path: str) -> None:
        inspection = self.inspect_ble_file(path)

        print("=" * 60)
        print("BASEBALL LANGUAGE ENGINE WORKBENCH")
        print("=" * 60)

        print()
        print("FILE")
        print("-" * 60)
        print(inspection["path"])

        print()
        print("SOURCE")
        print("-" * 60)
        print(inspection["source"])

        print()
        print("CLEANER")
        print("-" * 60)
        print(
            f"{len(inspection['cleaned_plate_appearances'])} cleaned plate appearances"
        )

        print()
        print("GAME")
        print("-" * 60)
        print(
            f"{inspection['plate_appearance_count']} parsed plate appearances"
        )
        print(f"{len(inspection['players'])} players")

        print()
        print("PLAYERS")
        print("-" * 60)

        for player in inspection["players"]:
            print(player)

        print()
        print("RUNNER EVENTS")
        print("-" * 60)

        if inspection["runner_events"]:
            for event in inspection["runner_events"]:
                print(event)
        else:
            print("None")

        print()
        print("AGGREGATED STATS")
        print("-" * 60)

        for player in sorted(inspection["stats"]):
            print(player)
            print(inspection["stats"][player])
            print()


def main(argv: list[str] | None = None) -> int:

    args = argv if argv is not None else sys.argv[1:]

    if not args:
        print("Usage:")
        print("py -m tools.inspection.workbench <raw_game_file>")
        return 1

    Workbench().print_ble_file_inspection(args[0])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
