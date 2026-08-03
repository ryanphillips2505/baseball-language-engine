#!/usr/bin/env python3
"""Score Presto/college capture corpus eventization rate."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cleaners.college_cleaner import clean_college_text
from detectors.event_detector import detect_event_types
from translators.base_translator import detected_events_to_baseball_event

RAW_DIR = ROOT / "samples" / "college" / "presto" / "raw"
MANIFEST_PATH = ROOT / "samples" / "college" / "presto" / "manifest.json"
TARGET = 0.99


def score_text(raw_text: str) -> tuple[int, int, list[str]]:
    blocks = clean_college_text(raw_text)
    undet: list[str] = []
    ok = 0
    for block in blocks:
        be = detected_events_to_baseball_event(detect_event_types(block))
        if be is not None:
            ok += 1
        else:
            undet.append(block)
    return ok, len(blocks), undet


def iter_fixture_paths() -> list[Path]:
    return sorted(p for p in RAW_DIR.glob("*.txt") if p.is_file())


def main() -> int:
    fixtures = iter_fixture_paths()
    if not fixtures:
        print("No Presto fixtures yet under samples/college/presto/raw/")
        print("Paste games to begin the 99% corpus loop.")
        return 0

    total_ok = 0
    total_n = 0
    print(f"Target: {TARGET:.0%} eventization\n")

    for path in fixtures:
        ok, n, undet = score_text(path.read_text(encoding="utf-8"))
        total_ok += ok
        total_n += n
        rate = (ok / n) if n else 1.0
        flag = "OK" if rate >= TARGET else "BELOW"
        print(f"[{flag}] {path.name}: {ok}/{n} = {rate:.2%}")
        for line in undet[:10]:
            print(f"  UND {line}")
        if len(undet) > 10:
            print(f"  ... +{len(undet) - 10} more")

    overall = (total_ok / total_n) if total_n else 1.0
    print(f"\nCorpus: {total_ok}/{total_n} = {overall:.2%} (target {TARGET:.0%})")

    if MANIFEST_PATH.exists():
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        manifest["last_score"] = {
            "eventized": total_ok,
            "cleaned": total_n,
            "rate": round(overall, 6),
            "meets_target": overall >= TARGET,
        }
        MANIFEST_PATH.write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
        )

    return 0 if overall >= TARGET else 1


if __name__ == "__main__":
    raise SystemExit(main())
