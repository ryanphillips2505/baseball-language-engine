from pathlib import Path

from pipeline.process_game import process_game


def test_gc_xbh_location_regression():
    raw = Path(
        "samples/gamechanger/raw/gamechanger_pa_blocks.txt"
    ).read_text(encoding="utf-8")

    game = process_game(raw)

    xbh_locations = {
        pa.location
        for pa in game.plate_appearances
        if pa.baseball_event is not None
        and (
            "DOUBLE" in str(pa.baseball_event)
            or "TRIPLE" in str(pa.baseball_event)
            or "HOME_RUN" in str(pa.baseball_event)
        )
    }

    assert "LF" in xbh_locations or "CF" in xbh_locations or "RF" in xbh_locations
