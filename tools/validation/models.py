from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ValidationIssue:
    level: str
    check: str
    message: str
    index: int | None = None
    batter: str | None = None
    raw: str | None = None


@dataclass(frozen=True)
class ValidationMetrics:
    source: str
    plate_appearances: int
    players: int
    runner_events: int
    bip: int
    pitch_tokens: int
    warnings: int
    errors: int
    coverage_percent: float


@dataclass(frozen=True)
class ValidationReport:
    path: str
    source: str
    data: dict[str, Any]
    issues: list[ValidationIssue] = field(default_factory=list)
    metrics: ValidationMetrics | None = None
