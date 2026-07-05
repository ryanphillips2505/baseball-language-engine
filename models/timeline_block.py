from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class TimelineBlockType(str, Enum):
    PLATE_APPEARANCE = "plate_appearance"
    GAME_EVENT = "game_event"


@dataclass(frozen=True)
class TimelineBlock:
    block_type: TimelineBlockType
    raw_text: str
    source: Optional[str] = None
    inning: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class PlateAppearanceBlock(TimelineBlock):
    def __init__(
        self,
        raw_text: str,
        source: Optional[str] = None,
        inning: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
    ):
        object.__setattr__(self, "block_type", TimelineBlockType.PLATE_APPEARANCE)
        object.__setattr__(self, "raw_text", raw_text)
        object.__setattr__(self, "source", source)
        object.__setattr__(self, "inning", inning)
        object.__setattr__(self, "metadata", metadata or {})


@dataclass(frozen=True)
class GameEventBlock(TimelineBlock):
    event_type: Optional[str] = None

    def __init__(
        self,
        raw_text: str,
        event_type: Optional[str] = None,
        source: Optional[str] = None,
        inning: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
    ):
        object.__setattr__(self, "block_type", TimelineBlockType.GAME_EVENT)
        object.__setattr__(self, "raw_text", raw_text)
        object.__setattr__(self, "event_type", event_type)
        object.__setattr__(self, "source", source)
        object.__setattr__(self, "inning", inning)
        object.__setattr__(self, "metadata", metadata or {})
