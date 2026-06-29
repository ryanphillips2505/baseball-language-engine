from __future__ import annotations

from .comparison import ComparisonResult
from .comparison_summary_builder import summarize


def print_comparison(results: list[ComparisonResult]) -> None:

    summary = summarize(results)

    print("=" * 80)
    print("BLE SHADOW MODE")
    print("=" * 80)

    print(f"Players          : {summary.total_players}")
    print(f"Stats Compared   : {summary.total_stats}")
    print(f"Matched          : {summary.matched}")
    print(f"Mismatched       : {summary.mismatched}")
    print(f"Percent Match    : {summary.percent_match}%")

    print()

    if summary.mismatched == 0:
        print("No differences found.")
        return

    print("=" * 80)

    for result in results:

        if result.matches:
            continue

        print(
            f"{result.player:25}"
            f"{result.stat:15}"
            f"Legacy={result.legacy_value:<5}"
            f"BLE={result.ble_value}"
        )
