from __future__ import annotations

from dataclasses import dataclass

from models.pitch_decision import PitchOutcome


@dataclass(frozen=True)
class CountState:
    balls: int
    strikes: int


def advance_count(
    count: CountState,
    outcome: PitchOutcome,
) -> tuple[CountState, bool]:
    """
    Advance count after a pitch.

    Returns:

    (
        new_count,
        plate_appearance_over,
    )
    """

    balls = count.balls
    strikes = count.strikes

    if outcome == PitchOutcome.BALL:
        balls += 1
        return CountState(min(balls, 4), strikes), balls >= 4

    if outcome == PitchOutcome.CALLED_STRIKE:
        strikes += 1
        return CountState(balls, min(strikes, 3)), strikes >= 3

    if outcome == PitchOutcome.SWING_MISS:
        strikes += 1
        return CountState(balls, min(strikes, 3)), strikes >= 3

    if outcome == PitchOutcome.FOUL:
        if strikes < 2:
            strikes += 1

        return CountState(balls, strikes), False

    if outcome == PitchOutcome.BIP:
        return CountState(balls, strikes), True

    return CountState(balls, strikes), False


__all__ = [
    "CountState",
    "advance_count",
]