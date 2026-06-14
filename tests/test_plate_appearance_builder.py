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