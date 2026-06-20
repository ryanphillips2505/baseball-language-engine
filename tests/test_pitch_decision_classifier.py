from classifiers.pitch_decision_classifier import classify_pitch_decision
from models.pitch_decision import PitchOutcome


def test_classifies_ball_tokens():
    assert classify_pitch_decision("Ball 1") == PitchOutcome.BALL
    assert classify_pitch_decision("Ball 2") == PitchOutcome.BALL


def test_classifies_called_strike_tokens():
    assert classify_pitch_decision("Called Strike") == PitchOutcome.CALLED_STRIKE
    assert classify_pitch_decision("Strike Looking") == PitchOutcome.CALLED_STRIKE
    assert classify_pitch_decision("Strike 1 looking") == PitchOutcome.CALLED_STRIKE


def test_classifies_swing_miss_tokens():
    assert classify_pitch_decision("Swinging Strike") == PitchOutcome.SWING_MISS
    assert classify_pitch_decision("Strike 2 swinging") == PitchOutcome.SWING_MISS


def test_classifies_foul_tokens():
    assert classify_pitch_decision("Foul") == PitchOutcome.FOUL
    assert classify_pitch_decision("Foul tip") == PitchOutcome.FOUL
    assert classify_pitch_decision("Foul bunt") == PitchOutcome.FOUL
    assert classify_pitch_decision("Bunt foul") == PitchOutcome.FOUL


def test_classifies_in_play_token():
    assert classify_pitch_decision("In play") == PitchOutcome.BIP


def test_unknown_token_returns_none():
    assert classify_pitch_decision("Pickoff attempt") is None