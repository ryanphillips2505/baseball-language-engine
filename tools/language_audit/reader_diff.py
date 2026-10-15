"""
Compare the legacy reader with the multi-platform reader on every
non-GameChanger sample, play by play.

Lists every play where the multi-platform reader changes a reading
(event, batter, ball type, location, ball in play), so each change can
be reviewed as an improvement or a regression.

Usage:
    py -m tools.language_audit.reader_diff
"""

from __future__ import annotations

from pathlib import Path

from assemblers.plate_appearance_builder import build_plate_appearance
from cleaners.cleaner_router import CLEANERS
from detectors.source_detector import SourceType, detect_source
from language.reader import build_multi_platform_plate_appearance


ROOT = Path(__file__).resolve().parents[2]

SAMPLE_DIRS = [
    ROOT / "samples" / "college",
    ROOT / "samples" / "iscore",
    ROOT / "samples" / "mlb",
]


def _reading(pa) -> tuple:
    event = pa.baseball_event.primary_event.value if pa.baseball_event else None
    return (event, pa.batter_name, pa.ball_type, pa.location, pa.is_bip)


def main() -> int:
    changed = 0

    for directory in SAMPLE_DIRS:
        for path in sorted(directory.rglob("*.txt")):
            raw = path.read_text(encoding="utf-8")
            source = detect_source(raw)

            if source in (SourceType.GAMECHANGER, SourceType.UNKNOWN):
                continue

            print(f"== {path.relative_to(ROOT)} ({source.value})")

            for block in CLEANERS[source](raw):
                old = _reading(build_plate_appearance(block))
                new = _reading(build_multi_platform_plate_appearance(block))

                if old != new:
                    changed += 1
                    print(f"  {block[:110]}")
                    print(f"    old {old}")
                    print(f"    new {new}")

    print(f"changed plays: {changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
