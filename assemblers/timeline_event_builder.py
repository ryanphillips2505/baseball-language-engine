from __future__ import annotations

from models.timeline import Timeline


def append_game_event(
    timeline: Timeline,
    event,
) -> None:
    timeline.append(event)
