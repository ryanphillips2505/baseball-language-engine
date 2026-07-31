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

    # Optional fields populated when a source supplies them (e.g. MLB StatsAPI).
    pitch_type: str | None = None
    velocity_mph: float | None = None
    count_after: str | None = None
    pitcher_name: str | None = None
    batter_name: str | None = None