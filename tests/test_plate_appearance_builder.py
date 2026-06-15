from assemblers.plate_appearance_builder import build_plate_appearance
from models.types import EventType


def test_build_plate_appearance_from_college_single():
    pa = build_plate_appearance(
        "J. Walk singled to center."
    )

    assert pa.batter_name == "J. Walk"
    assert pa.baseball_event.primary_event == EventType.SINGLE
    assert pa.location == "CF"
    assert pa.pitches == []
    assert pa.is_bip is True

def test_build_plate_appearance_with_runner_event():
    pa = build_plate_appearance(
        "John Smith steals second base."
    )

    assert len(pa.runner_events) == 1
    assert pa.runner_events[0].event_type == "SB"
    assert pa.runner_events[0].base == "2B"

def test_build_plate_appearance_with_runner_identity():
    pa = build_plate_appearance(
        "John Smith steals second base."
    )

    assert len(pa.runner_events) == 1
    assert pa.runner_events[0].event_type == "SB"
    assert pa.runner_events[0].base == "2B"
    assert pa.runner_events[0].runner_name == "John Smith"