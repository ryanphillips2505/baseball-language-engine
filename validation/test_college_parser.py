from pathlib import Path

from pipeline.process_game import process_game


SAMPLE_PATH = Path("samples/college/raw/college_raw_game_01.txt")


def test_college_parser_sample_file_exists():
    assert SAMPLE_PATH.exists()


def test_college_parser_builds_game_object():
    raw_text = SAMPLE_PATH.read_text(encoding="utf-8")
    game = process_game(raw_text)

    assert game is not None
    assert len(game.plate_appearances) > 0


def test_college_parser_has_real_plate_appearances():
    raw_text = SAMPLE_PATH.read_text(encoding="utf-8")
    game = process_game(raw_text)

    batter_names = {
        pa.batter_name
        for pa in game.plate_appearances
        if pa.batter_name
    }

    assert len(batter_names) > 0