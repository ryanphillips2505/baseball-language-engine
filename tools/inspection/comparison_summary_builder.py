from __future__ import annotations

from .comparison import ComparisonResult
from .comparison_summary import ComparisonSummary


def summarize(
    results: list[ComparisonResult],
) -> ComparisonSummary:

    matched = sum(r.matches for r in results)
    mismatched = len(results) - matched

    return ComparisonSummary(
        total_players=len({r.player for r in results}),
        total_stats=len(results),
        matched=matched,
        mismatched=mismatched,
    )
