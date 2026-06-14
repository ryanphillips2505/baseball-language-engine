from __future__ import annotations

from dataclasses import dataclass, field

from models.baseball_event import BaseballEvent
from models.pitch_event import PitchEvent


@dataclass
class PlateAppearance:
    batter_name: str | None

    baseball_event: BaseballEvent | None

    pitches: list[PitchEvent] = field(default_factory=list)

    ball_type: str | None = None

    location: str | None = None
