from assemblers.plate_appearance_builder import build_plate_appearance
from models.types import EventType


def test_gamechanger_bunts_into_fielders_choice_to_catcher():
    text = (
        "Braxton Bacon bunts into fielder's choice, pitcher Dez Mittelstet "
        "to catcher Zerek Slater, Dax Sullivan out advancing to home, "
        "Cody Young advances to 2nd."
    )

    pa = build_plate_appearance(text)

    assert pa.batter_name == "Braxton Bacon"
    assert pa.is_bip is True
    assert pa.ball_type == "BUNT"
    assert pa.location == "C"
    assert pa.baseball_event.primary_event == EventType.FIELDERS_CHOICE
