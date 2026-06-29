from __future__ import annotations

from .comparison import compare_stats
from .comparison_printer import print_comparison


def compare(
    legacy_stats: dict,
    ble_stats: dict,
) -> None:

    results = compare_stats(
        legacy=legacy_stats,
        ble=ble_stats,
    )

    print_comparison(results)
