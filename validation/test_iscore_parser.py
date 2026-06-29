from pathlib import Path

from pipeline.process_game import process_game


SAMPLE_PATH = Path("samples/iscore/raw/iscore_raw_game_01.txt")


def test_iscore_parser_sample_exists():
    assert SAMPLE_PATH.exists()


def test_iscore_parser_builds_game():
    raw_text = SAMPLE_PATH.read_text(encoding="utf-8")

    game = process_game(raw_text)

    assert game is not None
    assert len(game.plate_appearances) > 0


def test_iscore_parser_has_players():
    raw_text = SAMPLE_PATH.read_text(encoding="utf-8")

    game = process_game(raw_text)

    players = {
        pa.batter_name
        for pa in game.plate_appearances
        if pa.batter_name
    }

    assert len(players) > 0