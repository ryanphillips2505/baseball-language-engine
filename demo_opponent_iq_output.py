from __future__ import annotations

import sys
from pathlib import Path
from typing import Callable

from adapters.opponent_iq_adapter import adapt_game_stats_to_opponent_iq
from aggregators.game_stat_aggregator import aggregate_game_stats
from assemblers.plate_appearance_builder import build_plate_appearance
from cleaners.college_cleaner import clean_college_text
from cleaners.gamechanger_cleaner import clean_gamechanger_text
from cleaners.iscore_cleaner import clean_iscore_text
from cleaners.mlb_cleaner import clean_mlb_text
from models.game import Game

from translators.damage_dataframe_builder import build_damage_dataframe
from translators.season_summary_dataframe_builder import (
    build_season_summary_dataframe,
)
from translators.season_summary_translator import (
    build_season_summary_rows,
)
from translators.spray_zone_dataframe_builder import (
    build_spray_zone_dataframe,
)
from translators.spray_zone_translator import build_spray_zone_rows

Cleaner = Callable[[str], list[str]]


CLEANERS: dict[str, Cleaner] = {
    "gamechanger": clean_gamechanger_text,
    "gc": clean_gamechanger_text,
    "mlb": clean_mlb_text,
    "iscore": clean_iscore_text,
    "college": clean_college_text,
}


HITTING_DISPLAY_ORDER = [
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
]


LOCATION_DISPLAY_ORDER = [
    "LF",
    "CF",
    "RF",
    "3B",
    "SS",
    "2B",
    "1B",
    "P",
    "C",
]


COMBO_DISPLAY_ORDER = [
    "GB-LF",
    "GB-CF",
    "GB-RF",
    "GB-3B",
    "GB-SS",
    "GB-2B",
    "GB-1B",
    "GB-P",
    "GB-C",
    "FB-LF",
    "FB-CF",
    "FB-RF",
    "FB-3B",
    "FB-SS",
    "FB-2B",
    "FB-1B",
    "FB-P",
    "FB-C",
    "BUNT-LF",
    "BUNT-CF",
    "BUNT-RF",
    "BUNT-3B",
    "BUNT-SS",
    "BUNT-2B",
    "BUNT-1B",
    "BUNT-P",
    "BUNT-C",
]


def _usage() -> None:
    print()
    print("Usage:")
    print("  py demo_opponent_iq_output.py <source> <file_path>")
    print()
    print("Sources:")
    for source in sorted(CLEANERS):
        print(f"  - {source}")
    print()
    print("Example:")
    print(
        "  py demo_opponent_iq_output.py gamechanger "
        "samples/yukon_norman_2026_03_02_raw.txt"
    )
    print()


def _format_nonzero_stats(
    stats: dict[str, int],
    display_order: list[str],
) -> str:
    parts = []

    for key in display_order:
        value = stats.get(key, 0)

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

    internal_game_stats = aggregate_game_stats(game)

    opponent_iq_stats = adapt_game_stats_to_opponent_iq(
        internal_game_stats
    )

    season_summary_rows = build_season_summary_rows(
        opponent_iq_stats
    )

    season_summary_df = build_season_summary_dataframe(
        season_summary_rows
    )

    damage_df = build_damage_dataframe(
        season_summary_rows
    )

    spray_zone_rows = build_spray_zone_rows(
        season_summary_rows
    )
    
    spray_zone_df = build_spray_zone_dataframe(
        spray_zone_rows
    )

    print()
    print("=" * 72)
    print("OPPONENT IQ ADAPTER OUTPUT DEMO")
    print("=" * 72)
    print(f"Source: {source_key}")
    print(f"File: {file_path}")
    print(f"Cleaned plays: {len(cleaned_blocks)}")
    print(f"Players found: {len(opponent_iq_stats)}")
    print(f"Season summary rows: {len(season_summary_rows)}")
    print(f"Damage rows: {len(damage_df)}")
    print(f"Spray zone rows: {len(spray_zone_rows)}")
    print(f"Spray zone dataframe rows: {len(spray_zone_df)}")

    print()
    print("FIRST DATAFRAME ROW")
    print(season_summary_df.iloc[0].to_dict())
    print()
    print("FIRST DAMAGE ROW")
    print(damage_df.iloc[0].to_dict())
    print("FIRST SPRAY ZONE ROW")
    print(spray_zone_rows[0])
    print()
    print("FIRST SPRAY ZONE DATAFRAME ROW")
    print(spray_zone_df.iloc[0].to_dict())

    print("=" * 72)
    print()

    for player, player_output in sorted(opponent_iq_stats.items()):
        hitting = player_output["hitting"]
        locations = player_output["locations"]
        combos = player_output["combos"]

        print(player)
        print("-" * len(player))

        print("HITTING")
        print(_format_nonzero_stats(hitting, HITTING_DISPLAY_ORDER))
        print()

        print("LOCATIONS")
        print(_format_nonzero_stats(locations, LOCATION_DISPLAY_ORDER))
        print()

        print("COMBOS")
        print(_format_nonzero_stats(combos, COMBO_DISPLAY_ORDER))
        print()

        print("=" * 72)
        print()

    print("Done.")
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