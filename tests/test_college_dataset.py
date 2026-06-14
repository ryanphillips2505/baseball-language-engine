from pathlib import Path

from cleaners.college_cleaner import clean_college_text
from detectors.event_detector import detect_event_types
from translators.base_translator import detected_events_to_baseball_event


def test_college_dataset_regression():
    raw_text = Path("samples/college_raw_game_01.txt").read_text()

    cleaned_blocks = clean_college_text(raw_text)

    valid_events = []

    for block in cleaned_blocks:
        detected = detect_event_types(block)
        baseball_event = detected_events_to_baseball_event(detected)

        assert baseball_event is not None
        valid_events.append(baseball_event)

    assert len(cleaned_blocks) == 72
    assert len(valid_events) == 72