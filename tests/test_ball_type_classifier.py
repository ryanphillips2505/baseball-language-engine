from classifiers.ball_type_classifier import classify_ball_type


def test_ground_ball_events():
    assert classify_ball_type(
        "grounded out to shortstop."
    ) == "GB"

    assert classify_ball_type(
        "singled on a ground ball to center."
    ) == "GB"


def test_fly_ball_events():
    assert classify_ball_type(
        "flied out to center."
    ) == "FB"

    assert classify_ball_type(
        "hits a line drive to left."
    ) == "FB"


def test_bunt_events():
    assert classify_ball_type(
        "bunts for an out."
    ) == "BUNT"


def test_non_bip_events():
    assert classify_ball_type(
        "walked."
    ) is None