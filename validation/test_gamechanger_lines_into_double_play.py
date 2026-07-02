from assemblers.plate_appearance_builder import build_plate_appearance
from models.types import EventType


def test_gamechanger_lines_into_double_play_to_pitcher_with_runner_doubled_off():
    text = (
        "Kaleb Crosby lines into a double play to pitcher S Walters, "
        "Jaylon Hill doubled off at 1st."
    )

    pa = build_plate_appearance(text)

    assert pa.batter_name == "Kaleb Crosby"
    assert pa.is_bip is True
    assert pa.ball_type == "FB"
    assert pa.location == "P"
    assert pa.baseball_event.primary_event == EventType.DOUBLE_PLAY
