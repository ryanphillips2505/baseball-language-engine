from pathlib import Path

from pipeline.process_game import process_game


def test_gc_caught_stealing_home_regression():
    raw = Path(
        "samples/gamechanger/raw/gamechanger_pa_blocks.txt"
    ).read_text(encoding="utf-8")

    game = process_game(raw)

    assert game is not None

    assert any(
        event.base == "HOME"
        for pa in game.plate_appearances
        for event in pa.runner_events
    )
