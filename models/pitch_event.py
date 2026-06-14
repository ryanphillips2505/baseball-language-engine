from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PitchEvent:
    pitch_number: int

    count_before: str | None

    result: str

    swing: bool | None

    ball_in_play: bool = False

    terminal_pitch: bool = False