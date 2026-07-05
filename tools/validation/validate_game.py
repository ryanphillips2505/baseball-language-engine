from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from tools.validation.report import print_validation_report
from tools.validation.validator import validate_game_file


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage:")
        print("  py tools/validation/validate_game.py <path-to-game-file>")
        return 1

    path = sys.argv[1]

    if not Path(path).exists():
        print(f"File not found: {path}")
        return 1

    report = validate_game_file(path)
    print_validation_report(report)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
