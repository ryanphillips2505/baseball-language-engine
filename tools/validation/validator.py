from __future__ import annotations

from tools.inspection.ble_inspector import inspect_ble_file

from .checks import run_validation_checks
from .metrics import build_validation_metrics
from .models import ValidationReport


def validate_game_file(path: str) -> ValidationReport:
    data = inspect_ble_file(path)
    issues = run_validation_checks(data)
    metrics = build_validation_metrics(data, issues)

    return ValidationReport(
        path=path,
        source=str(data.get("source", "unknown")),
        data=data,
        issues=issues,
        metrics=metrics,
    )
