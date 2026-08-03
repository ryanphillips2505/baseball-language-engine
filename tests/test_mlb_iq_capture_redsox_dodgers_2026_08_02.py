from __future__ import annotations

from pathlib import Path

from cleaners.mlb_cleaner import clean_mlb_text
from detectors.source_detector import detect_source
from models.types import EventType
from pipeline.process_game import process_game

FIXTURE = Path("samples/mlb/validation/redsox_dodgers_2026_08_02.txt")


def test_iq_capture_paste_detected_as_mlb():
    raw = FIXTURE.read_text(encoding="utf-8")
    assert detect_source(raw).value == "mlb"


def test_iq_capture_rejects_highlight_streak_caption():
    raw = FIXTURE.read_text(encoding="utf-8")
    lines = clean_mlb_text(raw)
    assert not any("extend hitting streak" in line.lower() for line in lines)
    assert "Freddie Freeman singles to extend hitting streak" not in lines


def test_iq_capture_keeps_official_play_lines():
    raw = FIXTURE.read_text(encoding="utf-8")
    lines = clean_mlb_text(raw)
    assert "Nick Sogard walks." in lines
    assert any("Ceddanne Rafaela homers" in line for line in lines)
    assert any("Jarren Duran out on a sacrifice bunt" in line for line in lines)
    assert any(
        "Shohei Ohtani advances to 2nd on defensive indifference" in line
        for line in lines
    )


def test_iq_capture_process_game_eventizes_all_pas():
    raw = FIXTURE.read_text(encoding="utf-8")
    game = process_game(raw)
    assert len(game.plate_appearances) == 82
    undet = [pa for pa in game.plate_appearances if pa.baseball_event is None]
    assert undet == []


def test_iq_capture_key_outcomes():
    raw = FIXTURE.read_text(encoding="utf-8")
    game = process_game(raw)
    events = [pa.baseball_event.primary_event for pa in game.plate_appearances]
    assert events.count(EventType.HOME_RUN) == 4
    assert events.count(EventType.INTENTIONAL_WALK) == 1
    assert events.count(EventType.SAC_BUNT) == 1
    assert events.count(EventType.ERROR) == 1
