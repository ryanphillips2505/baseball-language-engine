from __future__ import annotations

from pathlib import Path

from aggregators.game_stat_aggregator import aggregate_game_stats
from assemblers.game_builder import build_game
from cleaners.cleaner_router import clean_by_source
from cleaners.mlb_timeline_cleaner import clean_mlb_timeline_text
from detectors.source_detector import SourceType, detect_source
from pipeline.process_game import process_game


def inspect_ble_file(path: str) -> dict:
    file_path = Path(path)
    raw_text = file_path.read_text(encoding="utf-8")
    source = detect_source(raw_text)

    if source == SourceType.MLB:
        cleaned_timeline_blocks = clean_mlb_timeline_text(raw_text)
        game = build_game(cleaned_timeline_blocks)
        cleaned_plate_appearances = [
            block.raw_text
            for block in cleaned_timeline_blocks
            if block.block_type.value == "plate_appearance"
        ]
    else:
        cleaned_plate_appearances = clean_by_source(raw_text)
        cleaned_timeline_blocks = []
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

    timeline_game_events = []

    for block in getattr(game.timeline, "blocks", []) or []:
        if block.block_type.value != "game_event":
            continue

        event = block.metadata.get("game_event")

        timeline_game_events.append(
            {
                "event_type": getattr(event, "event_type", block.event_type),
                "runner_name": getattr(event, "runner_name", None),
                "base": getattr(event, "base", None),
                "from_base": getattr(event, "from_base", None),
                "to_base": getattr(event, "to_base", None),
                "outcome": getattr(event, "outcome", None),
                "raw": block.raw_text,
                "administrative": bool(
                    (block.metadata or {}).get("administrative")
                ),
            }
        )

    return {
        "path": str(file_path),
        "source": source.value,
        "cleaned_plate_appearances": cleaned_plate_appearances,
        "cleaned_timeline_blocks": cleaned_timeline_blocks,
        "game": game,
        "plate_appearance_count": len(game.plate_appearances),
        "timeline_count": len(getattr(game.timeline, "blocks", []) or []),
        "players": players,
        "stats": stats,
        "runner_events": runner_events,
        "timeline_game_events": timeline_game_events,
    }
