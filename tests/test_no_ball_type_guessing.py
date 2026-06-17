from assemblers.plate_appearance_builder import build_plate_appearance


def test_double_to_right_field_does_not_guess_ball_type():
    pa = build_plate_appearance(
        "John Smith doubled to right field."
    )

    assert pa.is_bip is True
    assert pa.location == "RF"
    assert pa.ball_type is None


def test_single_to_center_does_not_guess_ball_type():
    pa = build_plate_appearance(
        "John Smith singled to center."
    )

    assert pa.is_bip is True
    assert pa.location == "CF"
    assert pa.ball_type is None


def test_home_run_to_left_field_does_not_guess_ball_type():
    pa = build_plate_appearance(
        "John Smith homered to left field."
    )

    assert pa.is_bip is True
    assert pa.location == "LF"
    assert pa.ball_type is None
