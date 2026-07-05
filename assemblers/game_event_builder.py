from __future__ import annotations

import re

from models.game_event import GameEvent
from models.timeline_block import GameEventBlock


_BASE_RE = re.compile(
    r"\b(2nd|3rd|home) base\b",
    re.I,
)


def build_game_event(block: GameEventBlock) -> GameEvent:

    base_match = _BASE_RE.search(block.raw_text)

    return GameEvent(
        event_type=block.event_type or "unknown",
        raw_text=block.raw_text,
        base=base_match.group(1).lower() if base_match else None,
        source=block.source or "",
    )


__all__ = [
    "build_game_event",
]
