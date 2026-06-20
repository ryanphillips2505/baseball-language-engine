from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class PitchOutcome(str, Enum):
    BALL = "BALL"
    CALLED_STRIKE = "CALLED_STRIKE"
    SWING_MISS = "SWING_MISS"
    FOUL = "FOUL"
    BIP = "BIP"


@dataclass(frozen=True)
class PitchDecision:
    count: str
    outcome: PitchOutcome


__all__ = [
    "PitchDecision",
    "PitchOutcome",
]