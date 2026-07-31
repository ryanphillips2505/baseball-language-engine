from pathlib import Path

from assemblers.plate_appearance_builder import build_plate_appearance
from cleaners.mlb_cleaner import clean_mlb_text
from detectors.event_detector import detect_event_types
from models.types import EventType
from pipeline.process_game import process_game
from translators.base_translator import detected_events_to_baseball_event


SAC_BUNT_ROE = (
    "Jarren Duran hits a sacrifice bunt. Missed catch error by first baseman "
    "Nolan Schanuel, assist to pitcher Reid Detmers. Caleb Durbin scores. "
    "Romy Gonzalez to 3rd. Jarren Duran to 2nd."
)

SAC_BUNT_HIGHLIGHT_CAPTION = "Jarren Duran's sac bunt scores Caleb Durbin"


def test_mlb_cleaner_keeps_sacrifice_bunt_roe_play_line():
    cleaned = clean_mlb_text(SAC_BUNT_ROE)
    assert cleaned == [SAC_BUNT_ROE]


def test_mlb_cleaner_rejects_sac_bunt_highlight_caption():
    cleaned = clean_mlb_text(SAC_BUNT_HIGHLIGHT_CAPTION)
    assert cleaned == []


def test_mlb_sacrifice_bunt_roe_detects_as_sac_bunt_for_batter():
    detected = detect_event_types(SAC_BUNT_ROE)
    event = detected_events_to_baseball_event(detected)
    pa = build_plate_appearance(SAC_BUNT_ROE)

    assert event is not None
    assert event.primary_event == EventType.SAC_BUNT
    assert pa.batter_name == "Jarren Duran"
    assert pa.ball_type == "BUNT"
    assert pa.is_bip is True


def test_mlb_red_sox_angels_gameday_fixture_preserves_sacrifice_bunt_roe():
    raw = Path(
        "samples/mlb/validation/red_sox_angels_2026_07_04.txt"
    ).read_text(encoding="utf-8")

    cleaned = clean_mlb_text(raw)
    assert any("hits a sacrifice bunt" in line.lower() for line in cleaned)
    assert all("sac bunt scores" not in line.lower() for line in cleaned)

    game = process_game(raw)
    matching = [
        pa
        for pa in game.plate_appearances
        if pa.batter_name == "Jarren Duran"
        and pa.baseball_event
        and pa.baseball_event.primary_event == EventType.SAC_BUNT
    ]
    assert matching
    assert matching[0].ball_type == "BUNT"
