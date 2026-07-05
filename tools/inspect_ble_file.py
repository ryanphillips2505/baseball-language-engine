from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.inspection.ble_inspector import inspect_ble_file


def simplify(value):
    if isinstance(value, dict):
        return {k: simplify(v) for k, v in value.items()}
    if isinstance(value, list):
        return [simplify(v) for v in value]
    if hasattr(value, "value"):
        return value.value
    if hasattr(value, "__dict__"):
        return str(value)
    return value


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: py tools/inspect_ble_file.py <path>")
        return 2

    data = inspect_ble_file(sys.argv[1])

    summary = {
        "path": data["path"],
        "source": data["source"],
        "plate_appearance_count": data["plate_appearance_count"],
        "timeline_count": data["timeline_count"],
        "players": data["players"],
        "runner_events": data["runner_events"],
        "timeline_game_events": data["timeline_game_events"],
    }

    print(json.dumps(simplify(summary), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
