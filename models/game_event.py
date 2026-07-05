from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class GameEvent:
    event_type: str
    raw_text: str
    runner_name: str | None = None
    base: str | None = None
    source: str = ""

    inning: str | None = None
    actor_name: str | None = None
    target_name: str | None = None
    from_base: str | None = None
    to_base: str | None = None
    outcome: str | None = None
    credited_to: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
