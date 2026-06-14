from classifiers.bip_classifier import is_ball_in_play


def test_ground_ball_is_bip():
    assert is_ball_in_play("GB") is True


def test_fly_ball_is_bip():
    assert is_ball_in_play("FB") is True


def test_bunt_is_bip():
    assert is_ball_in_play("BUNT") is True


def test_none_is_not_bip():
    assert is_ball_in_play(None) is False
