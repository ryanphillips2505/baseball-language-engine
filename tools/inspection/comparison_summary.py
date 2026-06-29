from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ComparisonSummary:
    total_players: int
    total_stats: int
    matched: int
    mismatched: int

    @property
    def percent_match(self) -> float:
        if self.total_stats == 0:
            return 100.0

        return round(
            (self.matched / self.total_stats) * 100,
            2,
        )
