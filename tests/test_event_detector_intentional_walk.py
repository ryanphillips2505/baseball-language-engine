from detectors.event_detector import detect_event_types
from models.types import EventType


def test_detect_intentional_walk_as_walk():
    events = detect_event_types(
        "John Smith is intentionally walked."
    )

    assert events[0].event_type == EventType.WALK