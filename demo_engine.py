from __future__ import annotations

import sys
from pathlib import Path
from typing import Callable

from aggregators.game_stat_aggregator import aggregate_game_stats
from assemblers.plate_appearance_builder import build_plate_appearance
from cleaners.college_cleaner import clean_college_text
from cleaners.gamechanger_cleaner import clean_gamechanger_text
from cleaners.iscore_cleaner import clean_iscore_text
from cleaners.mlb_cleaner import clean_mlb_text
from models.game import Game


Cleaner = Callable[[str], list[str]]


CLEANERS: dict[str, Cleaner] = {
    "gamechanger": clean_gamechanger_text,
    "gc": clean_gamechanger_text,
    "mlb": clean_mlb_text,
    "iscore": clean_iscore_text,
    "college": clean_college_text,
}


STAT_DISPLAY_ORDER = [
    "GP",
    "K",
    "BB",
    "HBP",
    "2B",
    "3B",
    "HR",
    "XBH",
    "SB",
    "CS",
    "BIP",
    "GB",
    "FB",
    "BUNT",
    "LOC_LF",
    "LOC_CF",
    "LOC_RF",
    "LOC_3B",
    "LOC_SS",
    "LOC_2B",
    "LOC_1B",
    "LOC_P",
    "LOC_C",
]


def _usage() -> None:
    print()
    print("Usage:")
    print("  py demo_engine.py <source> <file_path>")
    print()
    print("Sources:")
    for source in sorted(CLEANERS):
        print(f"  - {source}")
    print()
    print("Examples:")
    print(
        "  py demo_engine.py gamechanger "
        "samples/yukon_norman_2026_03_02_raw.txt"
    )
    print("  py demo_engine.py iscore samples/iscore_raw_game_01.txt")
    print("  py demo_engine.py college samples/college_raw_game_01.txt")
    print("  py demo_engine.py mlb samples/mlb_pa_blocks.txt")
    print()


def _format_stat_line(player_stats: dict[str, int]) -> str:
    parts = []

    for key in STAT_DISPLAY_ORDER:
        value = player_stats.get(key, 0)

        if value:
            parts.append(f"{key}: {value}")

    if not parts:
        return "No tracked stats"

    return " | ".join(parts)


def run_demo(source: str, file_path: str) -> None:
    source_key = source.lower().strip()

    if source_key not in CLEANERS:
        print(f"Unknown source: {source}")
        _usage()
        raise SystemExit(1)

    path = Path(file_path)

    if not path.exists():
        print(f"File not found: {file_path}")
        raise SystemExit(1)

    raw_text = path.read_text()

    cleaner = CLEANERS[source_key]

    cleaned_blocks = cleaner(raw_text)

    game = Game(
        plate_appearances=[
            build_plate_appearance(block)
            for block in cleaned_blocks
        ]
    )

    stats = aggregate_game_stats(game)

    print()
    print("=" * 72)
    print("BASEBALL LANGUAGE ENGINE DEMO")
    print("=" * 72)
    print(f"Source: {source_key}")
    print(f"File: {file_path}")
    print(f"Cleaned plays: {len(cleaned_blocks)}")
    print(f"Players found: {len(stats)}")
    print("=" * 72)
    print()

    for player, player_stats in sorted(stats.items()):
        print(player)
        print(_format_stat_line(player_stats))
        print()

    print("=" * 72)
    print("Done.")
    print("=" * 72)
    print()


def main() -> None:
    if len(sys.argv) != 3:
        _usage()
        raise SystemExit(1)

    source = sys.argv[1]
    file_path = sys.argv[2]

    run_demo(source, file_path)


if __name__ == "__main__":
    main()