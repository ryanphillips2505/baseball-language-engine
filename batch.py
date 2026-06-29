from __future__ import annotations

import sys

from ble_batch import process_directory


def main() -> int:

    if len(sys.argv) != 2:
        print("Usage:")
        print("py batch.py <directory>")
        return 1

    stats = process_directory(sys.argv[1])

    print()

    print("=" * 60)
    print("BLE BATCH PROCESSOR")
    print("=" * 60)

    print(f"Players: {len(stats)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
