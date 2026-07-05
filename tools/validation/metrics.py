from __future__ import annotations

from .models import ValidationIssue, ValidationMetrics


def build_validation_metrics(data: dict, issues: list[ValidationIssue]) -> ValidationMetrics:
    game = data.get("game")
    plate_appearances = getattr(game, "plate_appearances", []) or []

    runner_events = 0
    bip = 0
    pitch_tokens = 0

    for pa in plate_appearances:
        runner_events += len(getattr(pa, "runner_events", []) or [])

        if bool(getattr(pa, "is_bip", False)):
            bip += 1

        pitch_tokens += len(getattr(pa, "pitches", []) or [])

    warnings = sum(1 for issue in issues if issue.level == "warning")
    errors = sum(1 for issue in issues if issue.level == "error")

    total_checks = max(len(plate_appearances), 1)
    failed_pas = {
        issue.index
        for issue in issues
        if issue.level == "error" and issue.index is not None
    }

    coverage_percent = ((total_checks - len(failed_pas)) / total_checks) * 100

    return ValidationMetrics(
        source=str(data.get("source", "unknown")),
        plate_appearances=int(data.get("plate_appearance_count", len(plate_appearances))),
        players=len(data.get("players", []) or []),
        runner_events=runner_events,
        bip=bip,
        pitch_tokens=pitch_tokens,
        warnings=warnings,
        errors=errors,
        coverage_percent=round(coverage_percent, 2),
    )
