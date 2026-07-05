from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GameEvent:
    event_type: str
    raw_text: str
    runner_name: str | None = None
    base: str | None = None
    source: str = ""
