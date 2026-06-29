from __future__ import annotations

from .comparison import ComparisonResult
from .comparison_summary_builder import summarize
from .shadow_models import ShadowResult


def build_shadow_result(
    results: list[ComparisonResult],
) -> ShadowResult:

    summary = summarize(results)

    return ShadowResult(
        summary=summary,
        passed=summary.mismatched == 0,
    )
