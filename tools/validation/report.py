from __future__ import annotations

from .models import ValidationReport


def _status(label: str, passed: bool) -> str:
    mark = "✓" if passed else "✗"
    return f"{mark} {label}"


def print_validation_report(report: ValidationReport) -> None:
    metrics = report.metrics
    issues = report.issues

    error_checks = {issue.check for issue in issues if issue.level == "error"}
    warning_checks = {issue.check for issue in issues if issue.level == "warning"}

    print()
    print("=" * 48)
    print("BLE VALIDATION REPORT")
    print("=" * 48)
    print()
    print(f"File: {report.path}")
    print(f"Source: {report.source}")
    print()

    if metrics:
        print("Summary")
        print("-" * 48)
        print(f"Plate Appearances : {metrics.plate_appearances}")
        print(f"Players           : {metrics.players}")
        print(f"BIP               : {metrics.bip}")
        print(f"Runner Events     : {metrics.runner_events}")
        print(f"Pitch Decisions   : {metrics.pitch_tokens}")
        print(f"Warnings          : {metrics.warnings}")
        print(f"Errors            : {metrics.errors}")
        print(f"Coverage          : {metrics.coverage_percent}%")
        print()

    print("Checks")
    print("-" * 48)
    print(_status("Batter extraction", "batter_extraction" not in error_checks))
    print(_status("Event detection", "event_detection" not in error_checks))
    print(_status("Ball type", "ball_type" not in warning_checks and "ball_type" not in error_checks))
    print(_status("Location", "location" not in warning_checks and "location" not in error_checks))
    print(_status("Runner events", "runner_events" not in error_checks))
    print(_status("Pitch tokens", True))
    print()

    if issues:
        print("Issues")
        print("-" * 48)

        for issue in issues:
            prefix = "ERROR" if issue.level == "error" else "WARN "
            index = f"PA {issue.index}" if issue.index is not None else "GAME"
            batter = f" | {issue.batter}" if issue.batter else ""
            print(f"{prefix} | {index}{batter} | {issue.check} | {issue.message}")

            if issue.raw:
                print(f"       Raw: {issue.raw}")

        print()
    else:
        print("Issues")
        print("-" * 48)
        print("No validation issues found.")
        print()

    print("=" * 48)
