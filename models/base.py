from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class BaseEvent:
    source: str = ""
    raw_text: str = ""
    confidence: float = 1.0
    warnings: list[str] = field(default_factory=list)
