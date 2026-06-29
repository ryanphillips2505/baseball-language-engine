from __future__ import annotations

from pathlib import Path

from aggregators.game_stat_aggregator import aggregate_game_stats
from cleaners.cleaner_router import clean_by_source
from detectors.source_detector import detect_source
from pipeline.process_game import process_game


def inspect_ble_file(path: str) -> dict:
    """
    Run the complete BLE pipeline on a raw game file.
    """

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
