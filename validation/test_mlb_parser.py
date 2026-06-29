from pathlib import Path

from models.types import EventType
from pipeline.process_game import process_game


SAMPLE_PATH = Path("samples/mlb/raw/mlb_athletics_angels_2026_06_20.txt")


def _game():
    raw_text = SAMPLE_PATH.read_text(encoding="utf-8")
    return process_game(raw_text)


def _find_pa(game, batter_name: str, event_type: EventType):
    for pa in game.plate_appearances:
        if (
            pa.batter_name == batter_name
            and pa.baseball_event
            and pa.baseball_event.primary_event == event_type
        ):
            return pa

    raise AssertionError(f"Could not find PA: {batter_name} / {event_type}")


def test_mlb_full_game_file_exists():
    assert SAMPLE_PATH.exists()


def test_mlb_parses_walk():
    game = _game()
    pa = _find_pa(game, "Zach Neto", EventType.WALK)

    assert pa.is_bip is False
    assert pa.ball_type is None
    assert pa.location is None


def test_mlb_parses_line_out_to_left():
    game = _game()
    pa = _find_pa(game, "Nolan Schanuel", EventType.LINE_OUT)

    assert pa.is_bip is True
    assert pa.ball_type == "FB"
    assert pa.location == "LF"


def test_mlb_parses_strikeout_swinging():
    game = _game()
    pa = _find_pa(game, "Jo Adell", EventType.STRIKEOUT_SWINGING)

    assert pa.is_bip is False
    assert pa.ball_type is None
    assert pa.location is None


def test_mlb_parses_ground_out_to_third():
    game = _game()
    pa = _find_pa(game, "Zack Gelof", EventType.GROUND_OUT)

    assert pa.is_bip is True
    assert pa.ball_type == "GB"
    assert pa.location == "3B"


def test_mlb_parses_single_line_drive_to_right():
    game = _game()
    pa = _find_pa(game, "Tyler Soderstrom", EventType.SINGLE)

    assert pa.is_bip is True
    assert pa.ball_type == "FB"
    assert pa.location == "RF"


def test_mlb_parses_fly_out_to_center():
    game = _game()
    pa = _find_pa(game, "Oswald Peraza", EventType.FLY_OUT)

    assert pa.is_bip is True
    assert pa.ball_type == "FB"
    assert pa.location == "CF"


def test_mlb_parses_home_run_to_center():
    game = _game()
    pa = _find_pa(game, "Lawrence Butler", EventType.HOME_RUN)

    assert pa.is_bip is True
    assert pa.ball_type == "FB"
    assert pa.location == "CF"


def test_mlb_parses_double_to_center():
    game = _game()
    pa = _find_pa(game, "Shea Langeliers", EventType.DOUBLE)

    assert pa.is_bip is True
    assert pa.ball_type == "FB"
    assert pa.location == "CF"
