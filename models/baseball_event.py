from dataclasses import dataclass
from models.types import EventType


@dataclass
class BaseballEvent:
    primary_event: EventType
    secondary_events: list[EventType]
