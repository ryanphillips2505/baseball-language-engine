from __future__ import annotations

import re

from models.game_event import GameEvent
from models.timeline_block import GameEventBlock


_RUNNER_RE = re.compile(
    r"^([A-Z][A-Za-z'.-]+(?:\s+[A-Z][A-Za-z'.-]+)+)",
)

_ADVANCE_RE = re.compile(
    r"\.\s*([A-Z][A-Za-z'.-]+(?:\s+[A-Z][A-Za-z'.-]+)+)\s+to\s+(1st|2nd|3rd|home)\b",
)

_BASE_RE = re.compile(
    r"\b(1st|2nd|3rd|home) base\b",
    re.I,
)


def _previous_base(to_base: str | None) -> str | None:
    if to_base == "2nd":
        return "1st"
    if to_base == "3rd":
        return "2nd"
    if to_base == "home":
        return "3rd"
    return None


def build_game_event(block: GameEventBlock) -> GameEvent:

    event_type = block.event_type or "unknown"
    runner_match = _RUNNER_RE.search(block.raw_text)
    advance_match = _ADVANCE_RE.search(block.raw_text)
    base_match = _BASE_RE.search(block.raw_text)

    runner_name = runner_match.group(1) if runner_match else None
    base = base_match.group(1).lower() if base_match else None
    to_base = None
    from_base = None
    outcome = None

    if event_type in {"stolen_base", "caught_stealing"}:
        to_base = base
        from_base = _previous_base(to_base)
        outcome = "safe" if event_type == "stolen_base" else "out"

    elif event_type == "pickoff":
        from_base = base
        outcome = "out"

    elif event_type in {"wild_pitch", "passed_ball", "balk", "defensive_indifference"}:
        if advance_match:
            runner_name = advance_match.group(1)
            to_base = advance_match.group(2).lower()
            from_base = _previous_base(to_base)
        outcome = "advance"

    return GameEvent(
        event_type=event_type,
        raw_text=block.raw_text,
        runner_name=runner_name,
        actor_name=runner_name,
        base=base,
        from_base=from_base,
        to_base=to_base,
        outcome=outcome,
        source=block.source or "",
    )


__all__ = [
    "build_game_event",
]
