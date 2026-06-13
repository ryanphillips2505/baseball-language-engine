from __future__ import annotations

from dataclasses import dataclass

from models.types import EventType


@dataclass
class DetectedEvent:
    event_type: EventType
    is_primary: bool = False
