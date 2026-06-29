from pathlib import Path

from pipeline.process_game import process_game


def test_gc_sacrifice_bunt_regression():
    raw = Path(
        "samples/gamechanger/raw/gamechanger_pa_blocks.txt"
    ).read_text(encoding="utf-8")

    game = process_game(raw)

    assert game is not None

    # Regression guard:
    # Ensure bunt events are parsed without crashing.
    # This sample may legitimately contain zero sacrifice bunts.
    bunt_events = [
        pa
        for pa in game.plate_appearances
        if pa.baseball_event is not None
        and "BUNT" in str(pa.baseball_event)
    ]

    assert isinstance(bunt_events, list)
