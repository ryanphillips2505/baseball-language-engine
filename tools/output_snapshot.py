"""
Freeze everything BLE reads out of a play-by-play file.

The snapshot captures, for every plate appearance, the batter, the
detected events, ball type, location, ball-in-play flag, pitch
decisions and runner events, plus every timeline game event, the raw
aggregated stats and the final Opponent IQ stats produced by the
legacy compatibility adapter.

Used by tests/test_frozen_source_outputs.py to prove that language
coverage work never changes what Opponent IQ reads from GameChanger.

Usage:
    py -m tools.output_snapshot write   # regenerate baselines
    py -m tools.output_snapshot check   # diff current output vs baselines
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, is_dataclass
from enum import Enum
from pathlib import Path

from adapters.legacy_process_game_text import process_game_text
from aggregators.game_stat_aggregator import aggregate_game_stats
from pipeline.process_game import process_game


ROOT = Path(__file__).resolve().parent.parent
BASELINE_DIR = ROOT / "tests" / "fixtures" / "output_baselines"

# Every GameChanger sample is frozen. These outputs feed the live
# Opponent IQ GameChanger reading and must never change by accident.
FROZEN_SAMPLES = {
    "gc_17_games_yukon_2026": "samples/gamechanger/gc_17_games_yukon_2026.txt",
    "gc_risin_shockers_2026_06_04": "samples/gamechanger/risin_shockers_2026_06_04.txt",
    "gc_pa_blocks": "samples/gamechanger/raw/gamechanger_pa_blocks.txt",
    "gc_yukon_norman_2026_03_02": "samples/gamechanger/raw/yukon_norman_2026_03_02_raw.txt",
}


def _plain(value):
    if isinstance(value, Enum):
        return value.value

    if is_dataclass(value) and not isinstance(value, type):
        return _plain(asdict(value))

    if isinstance(value, dict):
        return {str(_plain(k)): _plain(v) for k, v in value.items()}

    if isinstance(value, (list, tuple)):
        return [_plain(item) for item in value]

    if isinstance(value, set):
        return sorted(_plain(item) for item in value)

    return value


def snapshot_text(raw_text: str) -> dict:
    game = process_game(raw_text)

    plate_appearances = []

    for pa in game.plate_appearances:
        event = pa.baseball_event

        plate_appearances.append(
            {
                "batter": pa.batter_name,
                "primary": _plain(event.primary_event) if event else None,
                "secondary": _plain(event.secondary_events) if event else [],
                "ball_type": pa.ball_type,
                "location": pa.location,
                "is_bip": pa.is_bip,
                "pitches": _plain(pa.pitches),
                "runner_events": _plain(pa.runner_events),
            }
        )

    game_events = []

    for block in getattr(game.timeline, "blocks", []):
        game_event = block.metadata.get("game_event") if block.metadata else None

        if game_event is None:
            continue

        game_events.append(
            {
                "event_type": game_event.event_type,
                "runner": game_event.runner_name,
                "from_base": game_event.from_base,
                "to_base": game_event.to_base,
                "outcome": game_event.outcome,
            }
        )

    game_team, game_players = process_game_text(raw_text)

    return {
        "plate_appearances": plate_appearances,
        "game_events": game_events,
        "aggregate_stats": _plain(aggregate_game_stats(game)),
        "opponent_iq_team": _plain(game_team),
        "opponent_iq_players": _plain(game_players),
    }


def baseline_path(name: str) -> Path:
    return BASELINE_DIR / f"{name}.json"


def snapshot_sample(relative_path: str) -> dict:
    raw_text = (ROOT / relative_path).read_text(encoding="utf-8")
    # Round-trip through JSON so comparisons see exactly what is stored.
    return json.loads(json.dumps(snapshot_text(raw_text), sort_keys=True))


def write_baselines() -> None:
    BASELINE_DIR.mkdir(parents=True, exist_ok=True)

    for name, relative_path in FROZEN_SAMPLES.items():
        baseline_path(name).write_text(
            json.dumps(snapshot_sample(relative_path), indent=1, sort_keys=True),
            encoding="utf-8",
        )
        print(f"wrote {baseline_path(name).relative_to(ROOT)}")


def diff_against_baseline(name: str) -> list[str]:
    expected = json.loads(baseline_path(name).read_text(encoding="utf-8"))
    actual = snapshot_sample(FROZEN_SAMPLES[name])

    differences: list[str] = []

    exp_pas = expected["plate_appearances"]
    act_pas = actual["plate_appearances"]

    if len(exp_pas) != len(act_pas):
        differences.append(
            f"plate appearance count {len(exp_pas)} -> {len(act_pas)}"
        )

    for index, (exp_pa, act_pa) in enumerate(zip(exp_pas, act_pas)):
        if exp_pa != act_pa:
            differences.append(f"PA #{index}: {exp_pa} -> {act_pa}")

    for key in ("game_events", "aggregate_stats", "opponent_iq_team", "opponent_iq_players"):
        if expected[key] != actual[key]:
            differences.append(f"{key} changed")

    return differences


def check_baselines() -> int:
    failed = 0

    for name in FROZEN_SAMPLES:
        differences = diff_against_baseline(name)

        if differences:
            failed += 1
            print(f"CHANGED {name}")
            for line in differences[:25]:
                print(f"  {line}")
        else:
            print(f"ok      {name}")

    return 1 if failed else 0


def main(argv: list[str]) -> int:
    command = argv[1] if len(argv) > 1 else "check"

    if command == "write":
        write_baselines()
        return 0

    return check_baselines()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
