from __future__ import annotations

from classifiers.pitch_decision_classifier import classify_pitch_decision
from models.count_state import CountState, advance_count
from models.pitch_decision import PitchDecision


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


__all__ = [
    "build_pitch_decisions",
]