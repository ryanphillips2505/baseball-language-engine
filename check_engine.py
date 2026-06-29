from __future__ import annotations

import subprocess
import sys
import time


CHECKS = [
    ("Unit Tests", [sys.executable, "-m", "pytest"]),
    ("MLB Validation", [sys.executable, "-m", "tools.inspection.validate", "mlb"]),
    ("College Validation", [sys.executable, "-m", "tools.inspection.validate", "college"]),
    ("iScore Validation", [sys.executable, "-m", "tools.inspection.validate", "iscore"]),
    ("Regression Tests", [sys.executable, "-m", "tools.inspection.validate", "regression"]),
]


def main() -> int:
    print("=" * 70)
    print("BASEBALL LANGUAGE ENGINE HEALTH CHECK")
    print("=" * 70)

    overall_success = True
    overall_start = time.time()

    for name, command in CHECKS:
        print()
        print(f"[RUNNING] {name}")

        start = time.time()
        result = subprocess.call(command)
        elapsed = time.time() - start

        if result == 0:
            print(f"[PASS] {name} ({elapsed:.2f}s)")
        else:
            print(f"[FAIL] {name} ({elapsed:.2f}s)")
            overall_success = False

    print()
    print("=" * 70)

    total = time.time() - overall_start

    if overall_success:
        print("ENGINE STATUS : PASS")
    else:
        print("ENGINE STATUS : FAIL")

    print(f"TOTAL TIME    : {total:.2f}s")
    print("=" * 70)

    return 0 if overall_success else 1


if __name__ == "__main__":
    raise SystemExit(main())
