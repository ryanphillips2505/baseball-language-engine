from detectors.event_detector import detect_event_types
from models.types import EventType


def test_detect_intentional_walk_as_intentional_walk():
    events = detect_event_types(
        "John Smith is intentionally walked."
    )

    assert events[0].event_type == EventType.INTENTIONAL_WALK


def test_detect_pitcher_subject_intentional_walk():
    events = detect_event_types(
        "Marco Gonzales intentionally walks Junior Caminero. "
        "Yandy Díaz to 3rd. Jonathan Aranda to 2nd."
    )

    assert events[0].event_type == EventType.INTENTIONAL_WALK
