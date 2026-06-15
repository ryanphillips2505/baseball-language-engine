from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RunnerEvent:
    event_type: str
    base: str