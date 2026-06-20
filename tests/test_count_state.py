from models.count_state import CountState, advance_count
from models.pitch_decision import PitchOutcome


def test_ball_advances_count():
    count, pa_over = advance_count(
        CountState(0, 0),
        PitchOutcome.BALL,
    )

    assert count == CountState(1, 0)
    assert pa_over is False


def test_called_strike_advances_count():
    count, pa_over = advance_count(
        CountState(0, 0),
        PitchOutcome.CALLED_STRIKE,
    )

    assert count == CountState(0, 1)
    assert pa_over is False


def test_swing_miss_advances_count():
    count, pa_over = advance_count(
        CountState(0, 0),
        PitchOutcome.SWING_MISS,
    )

    assert count == CountState(0, 1)
    assert pa_over is False


def test_foul_advances_to_first_strike():
    count, pa_over = advance_count(
        CountState(0, 0),
        PitchOutcome.FOUL,
    )

    assert count == CountState(0, 1)
    assert pa_over is False


def test_foul_with_two_strikes_does_not_add_strike():
    count, pa_over = advance_count(
        CountState(1, 2),
        PitchOutcome.FOUL,
    )

    assert count == CountState(1, 2)
    assert pa_over is False


def test_in_play_ends_plate_appearance():
    count, pa_over = advance_count(
        CountState(2, 1),
        PitchOutcome.BIP,
    )

    assert count == CountState(2, 1)
    assert pa_over is True


def test_walk_ends_plate_appearance():
    count, pa_over = advance_count(
        CountState(3, 1),
        PitchOutcome.BALL,
    )

    assert count == CountState(4, 1)
    assert pa_over is True


def test_strikeout_on_called_strike():
    count, pa_over = advance_count(
        CountState(1, 2),
        PitchOutcome.CALLED_STRIKE,
    )

    assert count == CountState(1, 3)
    assert pa_over is True


def test_strikeout_on_swing_miss():
    count, pa_over = advance_count(
        CountState(2, 2),
        PitchOutcome.SWING_MISS,
    )

    assert count == CountState(2, 3)
    assert pa_over is True