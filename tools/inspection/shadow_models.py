from __future__ import annotations

from dataclasses import dataclass

from .comparison_summary import ComparisonSummary


@dataclass(slots=True)
class ShadowResult:
    summary: ComparisonSummary
    passed: bool

    @property
    def ready_for_production(self) -> bool:
        return self.passed
