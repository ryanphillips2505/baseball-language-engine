from assemblers.plate_appearance_builder import build_plate_appearance
from models.types import EventType


def test_gamechanger_bunts_and_reaches_error_by_pitcher_counts_gb_p():
    text = (
        "Kate Seaton bunts and reaches on an error by pitcher Grace Tonga, "
        "Ryen Bullock scores."
    )

    pa = build_plate_appearance(text)

    assert pa.batter_name == "Kate Seaton"
    assert pa.is_bip is True
    assert pa.ball_type == "GB"
    assert pa.location == "P"
    assert pa.baseball_event.primary_event == EventType.ERROR
