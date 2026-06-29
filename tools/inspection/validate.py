from __future__ import annotations

import subprocess
import sys
import time

VALIDATION_GROUPS = {
    "all": [],
    "mlb": [
        "validation/test_mlb_cleaner.py",
        "validation/test_mlb_parser.py",
        "validation/test_mlb_stats.py",
    ],
    "college": [
        "validation/test_college_cleaner.py",
        "validation/test_college_parser.py",
        "validation/test_college_stats.py",
    ],
    "iscore": [
        "validation/test_iscore_cleaner.py",
        "validation/test_iscore_parser.py",
        "validation/test_iscore_stats.py",
    ],
    "regression": [
        "validation/regression",
    ],
}


def run(group: str = "all") -> int:
    start = time.time()

    print("=" * 60)
    print("BASEBALL LANGUAGE ENGINE VALIDATION")
    print("=" * 60)
    print(f"Group : {group}")
    print()

    if group == "all":
        cmd = [sys.executable, "-m", "pytest"]
    else:
        tests = VALIDATION_GROUPS.get(group)

        if tests is None:
            print(f"Unknown validation group: {group}")
            print()
            print("Available groups:")

            for name in sorted(VALIDATION_GROUPS):
                print(f"  {name}")

            return 1

        cmd = [sys.executable, "-m", "pytest", *tests]

    result = subprocess.call(cmd)

    elapsed = time.time() - start

    print()
    print("=" * 60)

    if result == 0:
        print("STATUS : PASS")
    else:
        print("STATUS : FAIL")

    print(f"TIME   : {elapsed:.2f} sec")
    print("=" * 60)

    return result


def main() -> int:
    group = sys.argv[1] if len(sys.argv) > 1 else "all"
    return run(group)


if __name__ == "__main__":
    raise SystemExit(main())
