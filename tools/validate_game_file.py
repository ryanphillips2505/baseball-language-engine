from __future__ import annotations

from dataclasses import asdict
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.validation.validator import validate_game_file


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: py tools/validate_game_file.py <path>")
        return 2

    report = validate_game_file(sys.argv[1])

    print("PATH")
    print(report.path)
    print()

    print("SOURCE")
    print(report.source)
    print()

    print("METRICS")
    if report.metrics is not None:
        for key, value in asdict(report.metrics).items():
            print(f"{key}: {value}")
    print()

    print("ISSUES")
    if report.issues:
        for issue in report.issues:
            issue_data = asdict(issue)
            print(
                f"- [{issue_data['level']}] "
                f"{issue_data['check']}: "
                f"{issue_data['message']}"
            )
    else:
        print("No issues found.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
