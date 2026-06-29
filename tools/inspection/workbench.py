from __future__ import annotations

import sys
from pathlib import Path

from aggregators.game_stat_aggregator import aggregate_game_stats
from cleaners.cleaner_router import clean_by_source
from detectors.source_detector import detect_source
from pipeline.process_game import process_game

from .game_inspector import build_game_inspection
from .game_loader import load_game_file
from .models import GameInspection, PlayInspection
from .play_inspector import build_play_inspection
from .printers import print_game_inspection, print_play_inspection


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

    def inspect_ble_file(self, path: str) -> dict:
        file_path = Path(path)
        raw_text = file_path.read_text(encoding="utf-8")

        source = detect_source(raw_text)
        cleaned_plate_appearances = clean_by_source(raw_text)
        game = process_game(raw_text)
        stats = aggregate_game_stats(game)

        players = sorted(
            {
                pa.batter_name
                for pa in game.plate_appearances
                if pa.batter_name
            }
        )

        runner_events = []
        for pa in game.plate_appearances:
            for runner_event in getattr(pa, "runner_events", []) or []:
                runner_events.append(
                    {
                        "batter": pa.batter_name,
                        "event_type": runner_event.event_type,
                        "base": runner_event.base,
                        "runner_name": runner_event.runner_name,
                    }
                )

        return {
            "path": str(file_path),
            "source": source.value,
            "cleaned_plate_appearances": cleaned_plate_appearances,
            "game": game,
            "plate_appearance_count": len(game.plate_appearances),
            "players": players,
            "stats": stats,
            "runner_events": runner_events,
        }

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
        print(f"{len(inspection['cleaned_plate_appearances'])} cleaned plate appearances")

        print()
        print("GAME OBJECT")
        print("-" * 60)
        print(f"{inspection['plate_appearance_count']} parsed plate appearances")
        print(f"{len(inspection['players'])} players")

        print()
        print("PLAYERS")
        print("-" * 60)
        for player in inspection["players"]:
            print(player)

        print()
        print("RUNNER EVENTS")
        print("-" * 60)
        if not inspection["runner_events"]:
            print("None")
        else:
            for event in inspection["runner_events"]:
                runner_name = event["runner_name"] or "UNKNOWN"
                print(
                    f"{event['event_type']} {event['base']} | "
                    f"runner={runner_name} | batter={event['batter']}"
                )

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
        print("  py -m tools.inspection.workbench <path-to-raw-game-file>")
        return 1

    path = args[0]

    workbench = Workbench()
    workbench.print_ble_file_inspection(path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())