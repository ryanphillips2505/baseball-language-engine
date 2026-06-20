from assemblers.pitch_decision_builder import build_pitch_decisions
from models.pitch_decision import PitchDecision, PitchOutcome


def test_builds_pitch_decisions_with_counts():
    decisions = build_pitch_decisions(
        [
            "Ball 1",
            "Strike 1 looking",
            "Foul",
            "In play",
        ]
    )

    assert decisions == [
        PitchDecision("0-0", PitchOutcome.BALL),
        PitchDecision("1-0", PitchOutcome.CALLED_STRIKE),
        PitchDecision("1-1", PitchOutcome.FOUL),
        PitchDecision("1-2", PitchOutcome.BIP),
    ]


def test_stops_after_in_play():
    decisions = build_pitch_decisions(
        [
            "In play",
            "Ball 1",
        ]
    )

    assert decisions == [
        PitchDecision("0-0", PitchOutcome.BIP),
    ]


def test_stops_after_walk():
    decisions = build_pitch_decisions(
        [
            "Ball 1",
            "Ball 2",
            "Ball 3",
            "Ball 4",
            "In play",
        ]
    )

    assert decisions == [
        PitchDecision("0-0", PitchOutcome.BALL),
        PitchDecision("1-0", PitchOutcome.BALL),
        PitchDecision("2-0", PitchOutcome.BALL),
        PitchDecision("3-0", PitchOutcome.BALL),
    ]


def test_foul_with_two_strikes_keeps_same_count():
    decisions = build_pitch_decisions(
        [
            "Strike 1 looking",
            "Strike 2 swinging",
            "Foul",
            "Foul",
            "In play",
        ]
    )

    assert decisions == [
        PitchDecision("0-0", PitchOutcome.CALLED_STRIKE),
        PitchDecision("0-1", PitchOutcome.SWING_MISS),
        PitchDecision("0-2", PitchOutcome.FOUL),
        PitchDecision("0-2", PitchOutcome.FOUL),
        PitchDecision("0-2", PitchOutcome.BIP),
    ]


def test_ignores_unknown_tokens():
    decisions = build_pitch_decisions(
        [
            "Pickoff attempt",
            "Ball 1",
        ]
    )

    assert decisions == [
        PitchDecision("0-0", PitchOutcome.BALL),
    ]