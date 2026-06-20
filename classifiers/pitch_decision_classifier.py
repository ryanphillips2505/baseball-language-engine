from __future__ import annotations

from models.pitch_decision import PitchOutcome


def classify_pitch_decision(token: str) -> PitchOutcome | None:
    """
    Convert a pitch token into a standardized PitchOutcome.

    Examples:

    Ball 1
    Ball 2
    -> BALL

    Strike 1 looking
    Called Strike
    Strike Looking
    -> CALLED_STRIKE

    Strike 2 swinging
    Swinging Strike
    -> SWING_MISS

    Foul
    Foul tip
    Foul bunt
    Bunt foul
    -> FOUL

    In play
    -> BIP
    """

    text = str(token or "").strip().lower()

    if not text:
        return None

    #
    # BALL
    #

    if text.startswith("ball "):
        return PitchOutcome.BALL

    #
    # CALLED STRIKE
    #

    if text in {
        "called strike",
        "strike looking",
    }:
        return PitchOutcome.CALLED_STRIKE

    if text.startswith("strike ") and "looking" in text:
        return PitchOutcome.CALLED_STRIKE

    #
    # SWING AND MISS
    #

    if text == "swinging strike":
        return PitchOutcome.SWING_MISS

    if text.startswith("strike ") and "swinging" in text:
        return PitchOutcome.SWING_MISS

    #
    # FOUL
    #

    if text in {
        "foul",
        "foul tip",
        "foul bunt",
        "bunt foul",
    }:
        return PitchOutcome.FOUL

    #
    # BALL IN PLAY
    #

    if text == "in play":
        return PitchOutcome.BIP

    return None


__all__ = [
    "classify_pitch_decision",
]