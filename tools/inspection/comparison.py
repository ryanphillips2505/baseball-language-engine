from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class ComparisonResult:
    player: str
    stat: str
    legacy_value: Any
    ble_value: Any

    @property
    def matches(self) -> bool:
        return self.legacy_value == self.ble_value


def compare_stats(
    legacy: dict[str, dict[str, Any]],
    ble: dict[str, dict[str, Any]],
) -> list[ComparisonResult]:

    results: list[ComparisonResult] = []

    players = sorted(set(legacy) | set(ble))

    for player in players:

        legacy_stats = legacy.get(player, {})
        ble_stats = ble.get(player, {})

        stats = sorted(set(legacy_stats) | set(ble_stats))

        for stat in stats:

            results.append(
                ComparisonResult(
                    player=player,
                    stat=stat,
                    legacy_value=legacy_stats.get(stat, 0),
                    ble_value=ble_stats.get(stat, 0),
                )
            )

    return results
