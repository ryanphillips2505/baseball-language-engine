from __future__ import annotations

from classifiers.pitch_decision_classifier import classify_pitch_decision
from classifiers.statsapi_pitch_decision_classifier import (
    classify_statsapi_pitch_result,
)
from models.count_state import CountState, advance_count
from models.pitch_decision import PitchDecision
from models.pitch_event import PitchEvent


def build_pitch_decisions(tokens: list[str]) -> list[PitchDecision]:
    decisions: list[PitchDecision] = []

    count = CountState(0, 0)
    pa_over = False

    for token in tokens:
        if pa_over:
            break

        outcome = classify_pitch_decision(token)

        if outcome is None:
            continue

        count_key = f"{count.balls}-{count.strikes}"

        decisions.append(
            PitchDecision(
                count=count_key,
                outcome=outcome,
            )
        )

        count, pa_over = advance_count(count, outcome)

    return decisions


def build_pitch_decisions_from_pitch_events(
    pitches: list[PitchEvent],
) -> list[PitchDecision]:
    """
    Convert structured StatsAPI PitchEvents into swing-report PitchDecisions.

    Uses each event's count_before (pre-pitch count) and mapped call outcome.
    Unmapped pitches such as HBP are skipped.
    """

    decisions: list[PitchDecision] = []

    for pitch in pitches:
        outcome = classify_statsapi_pitch_result(
            pitch.result,
            ball_in_play=bool(pitch.ball_in_play),
        )
        if outcome is None:
            continue

        count = pitch.count_before or "0-0"
        decisions.append(
            PitchDecision(
                count=count,
                outcome=outcome,
            )
        )

    return decisions


__all__ = [
    "build_pitch_decisions",
    "build_pitch_decisions_from_pitch_events",
]