from assemblers.plate_appearance_builder import build_plate_appearance


def test_gamechanger_pops_into_double_play_counts_as_fly_ball_bip_left_field():
    text = (
        "Dax Sullivan pops into a double play, left fielder Chris Daniels "
        "to pitcher Rock Gilliam to shortstop Owen Gilliam, "
        "Dawson Madden doubled off at 2nd."
    )

    pa = build_plate_appearance(text)

    assert pa.batter_name == "Dax Sullivan"
    assert pa.is_bip is True
    assert pa.ball_type == "FB"
    assert pa.location == "LF"
