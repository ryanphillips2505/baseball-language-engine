from __future__ import annotations

import re

from models.game_event import GameEvent
from models.timeline_block import GameEventBlock


_RUNNER_RE = re.compile(
    r"^([A-Z][A-Za-z'.-]+(?:\s+[A-Z][A-Za-z'.-]+)+)",
)

_BASE_RE = re.compile(
    r"\b(1st|2nd|3rd|home) base\b",
    re.I,
)


def build_game_event(block: GameEventBlock) -> GameEvent:

    runner_match = _RUNNER_RE.search(block.raw_text)
    base_match = _BASE_RE.search(block.raw_text)

    return GameEvent(
        event_type=block.event_type or "unknown",
        raw_text=block.raw_text,
        runner_name=runner_match.group(1) if runner_match else None,
        base=base_match.group(1).lower() if base_match else None,
        source=block.source or "",
    )


__all__ = [
    "build_game_event",
]
