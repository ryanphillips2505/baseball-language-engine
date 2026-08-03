from __future__ import annotations

from pathlib import Path

from extractors.mlb_iq_capture_names import build_box_to_pbp_name_map
from models.types import EventType
from pipeline.process_game import process_game

FIXTURE = Path("samples/mlb/validation/redsox_athletics_2026_07_30.txt")


def test_redsox_athletics_copy_paste_process_game():
    raw = FIXTURE.read_text(encoding="utf-8")
    game = process_game(raw)
    assert len(game.plate_appearances) == 74
    assert all(pa.baseball_event is not None for pa in game.plate_appearances)

    events = [pa.baseball_event.primary_event for pa in game.plate_appearances]
    assert events.count(EventType.HOME_RUN) == 2
    assert events.count(EventType.SAC_FLY) == 1
    assert events.count(EventType.SAC_BUNT) == 1


def test_redsox_athletics_box_to_pbp_name_map():
    raw = FIXTURE.read_text(encoding="utf-8")
    mapping = build_box_to_pbp_name_map(raw)
    assert mapping["Seigler2B"] == "Anthony Seigler"
    assert mapping["Butler, LCF"] == "Lawrence Butler"
    assert mapping["1-BoltePR"] == "Henry Bolte"
    assert mapping["a-WilliamsPH"] == "Alika Williams"
    assert mapping["ServenC"] == "Brian Serven"
    assert len(mapping) == 22
