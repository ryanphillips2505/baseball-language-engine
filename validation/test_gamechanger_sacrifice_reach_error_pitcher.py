from assemblers.plate_appearance_builder import build_plate_appearance


def test_gamechanger_sacrifices_and_reaches_on_error_by_pitcher_not_bunt_location():
    text = (
        "Charles Copus sacrifices and reaches on an error by pitcher "
        "Dekklyn Henslee, Wyatt Jones advances to 2nd."
    )

    pa = build_plate_appearance(text)

    assert pa.batter_name == "Charles Copus"
    assert pa.is_bip is True
    assert pa.ball_type is None
    assert pa.location is None
