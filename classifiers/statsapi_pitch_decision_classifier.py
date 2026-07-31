from __future__ import annotations

from models.pitch_decision import PitchOutcome


# Official StatsAPI call descriptions observed in live-feed fixtures, plus
# automatic variants the extractor already recognizes.
_BALL_RESULTS = {
    "ball",
    "ball in dirt",
    "automatic ball",
}

_CALLED_STRIKE_RESULTS = {
    "called strike",
    "automatic strike",
}

_SWING_MISS_RESULTS = {
    "swinging strike",
    "swinging strike (blocked)",
}

_FOUL_RESULTS = {
    "foul",
    "foul tip",
    "foul bunt",
}

# Present in PitchOutcome vocabulary for GC tokens, but HBP is not a swing
# decision bucket — skip rather than force a BALL classification.
_SKIP_RESULTS = {
    "hit by pitch",
}


def classify_statsapi_pitch_result(
    result: str,
    *,
    ball_in_play: bool = False,
) -> PitchOutcome | None:
    """
    Map an MLB StatsAPI pitch call description to PitchOutcome.

    Prefer call description text already extracted onto PitchEvent.result.
    Ball-in-play flag covers In play, out(s)/no out/run(s) variants.
    Returns None for unmapped / non-decision pitches (e.g. HBP).
    """

    text = str(result or "").strip().lower()
    if not text and not ball_in_play:
        return None

    if ball_in_play or text.startswith("in play"):
        return PitchOutcome.BIP

    if text in _SKIP_RESULTS:
        return None

    if text in _BALL_RESULTS:
        return PitchOutcome.BALL

    if text in _CALLED_STRIKE_RESULTS:
        return PitchOutcome.CALLED_STRIKE

    if text in _SWING_MISS_RESULTS:
        return PitchOutcome.SWING_MISS

    if text in _FOUL_RESULTS:
        return PitchOutcome.FOUL

    return None


__all__ = [
    "classify_statsapi_pitch_result",
]
