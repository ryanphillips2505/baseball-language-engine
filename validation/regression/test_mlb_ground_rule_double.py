from cleaners.mlb_cleaner import clean_mlb_text
from detectors.event_detector import detect_event_types
from extractors.player_extractor import extract_batter_name
from models.types import EventType
from translators.base_translator import detected_events_to_baseball_event


GROUND_RULE_DOUBLE = (
    "Ceddanne Rafaela hits a ground-rule double (13) "
    "on a line drive to right field."
)


def test_mlb_cleaner_keeps_ground_rule_double_wording():
    cleaned = clean_mlb_text(GROUND_RULE_DOUBLE)

    assert cleaned == [GROUND_RULE_DOUBLE]


def test_mlb_ground_rule_double_detects_as_double():
    detected = detect_event_types(GROUND_RULE_DOUBLE)
    event = detected_events_to_baseball_event(detected)

    assert event is not None
    assert event.primary_event == EventType.DOUBLE


def test_mlb_ground_rule_double_assigns_batter():
    assert extract_batter_name(GROUND_RULE_DOUBLE) == "Ceddanne Rafaela"


def test_mlb_pa_blocks_fixture_preserves_ground_rule_double():
    from pathlib import Path

    raw = Path("samples/mlb/raw/mlb_pa_blocks.txt").read_text(encoding="utf-8")
    cleaned = clean_mlb_text(raw)

    assert any("ground-rule double" in line.lower() for line in cleaned)
