from models.baseball_event import BaseballEvent
from models.pitch_event import PitchEvent
from models.plate_appearance import PlateAppearance
from models.types import EventType


def test_plate_appearance_model():
    pitch = PitchEvent(
        pitch_number=1,
        count_before="0-0",
        result="Strike Looking",
        swing=False,
    )

    event = BaseballEvent(
        primary_event=EventType.STRIKEOUT_LOOKING,
        secondary_events=[],
    )

    pa = PlateAppearance(
        batter_name="J. Walk",
        baseball_event=event,
        pitches=[pitch],
        ball_type="FB",
        location="CF",
    )

    assert pa.batter_name == "J. Walk"
    assert pa.baseball_event.primary_event == EventType.STRIKEOUT_LOOKING
    assert len(pa.pitches) == 1
    assert pa.ball_type == "FB"
    assert pa.location == "CF"