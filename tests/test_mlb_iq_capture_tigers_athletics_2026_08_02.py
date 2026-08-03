from __future__ import annotations

from pathlib import Path

from cleaners.mlb_cleaner import clean_mlb_text
from extractors.mlb_iq_capture_names import build_box_to_pbp_name_map
from models.types import EventType
from pipeline.process_game import process_game

FIXTURE = Path("samples/mlb/validation/tigers_athletics_2026_08_02.txt")


def test_tigers_athletics_iq_capture_rejects_abs_and_end_game_captions():
    raw = FIXTURE.read_text(encoding="utf-8")
    lines = clean_mlb_text(raw)
    assert "Ben Malgeri walks after ABS Challenge" not in lines
    assert "Enmanuel De Jesus strikes out Henry Bolte to end game" not in lines


def test_tigers_athletics_iq_capture_process_game():
    raw = FIXTURE.read_text(encoding="utf-8")
    game = process_game(raw)
    assert len(game.plate_appearances) == 84
    assert all(pa.baseball_event is not None for pa in game.plate_appearances)

    events = [pa.baseball_event.primary_event for pa in game.plate_appearances]
    assert events.count(EventType.HOME_RUN) == 1
    assert events.count(EventType.DOUBLE) == 4
    assert events.count(EventType.HIT_BY_PITCH) == 2


def test_tigers_athletics_box_to_pbp_name_map():
    raw = FIXTURE.read_text(encoding="utf-8")
    mapping = build_box_to_pbp_name_map(raw)
    assert mapping["Torres2B"] == "Gleyber Torres"
    assert mapping["Butler, LRF"] == "Lawrence Butler"
    assert mapping["CortesDH-P"] == "Carlos Cortes"
    assert mapping["a-KeithPH"] == "Colt Keith"
    assert mapping["b-ServenPH"] == "Brian Serven"
    assert len(mapping) == 22
