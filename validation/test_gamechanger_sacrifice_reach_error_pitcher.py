from assemblers.plate_appearance_builder import build_plate_appearance
from models.types import EventType


def test_gamechanger_sacrifices_and_reaches_on_error_by_pitcher_understands_bunt_error():
    text = (
        "Charles Copus sacrifices and reaches on an error by pitcher "
        "Dekklyn Henslee, Wyatt Jones advances to 2nd."
    )

    pa = build_plate_appearance(text)

    assert pa.batter_name == "Charles Copus"
    assert pa.is_bip is True
    assert pa.ball_type == "BUNT"
    assert pa.location is None
    assert pa.baseball_event.primary_event == EventType.ERROR
    assert EventType.SAC_BUNT in pa.baseball_event.secondary_events
