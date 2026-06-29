from pathlib import Path

from pipeline.process_game import process_game


def test_gc_foul_bunt_regression():
    raw = Path(
        "samples/gamechanger/raw/gamechanger_pa_blocks.txt"
    ).read_text(encoding="utf-8")

    game = process_game(raw)

    assert game is not None

    assert any(
        pa.baseball_event is not None
        for pa in game.plate_appearances
    )
