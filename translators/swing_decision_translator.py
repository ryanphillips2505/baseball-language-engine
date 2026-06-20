from __future__ import annotations

from aggregators.swing_decision_aggregator import COUNT_ORDER


def _pct(numerator: int, denominator: int) -> float:
    if denominator <= 0:
        return 0.0

    return numerator / denominator


def build_swing_decision_rows(
    swing_stats: dict[str, dict[str, dict[str, int]]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    for player_name in sorted(swing_stats.keys()):
        player_counts = swing_stats[player_name]

        for count in COUNT_ORDER:
            bucket = player_counts[count]

            pa = int(bucket["PA"])
            bip = int(bucket["BIP"])
            swing_miss = int(bucket["SWING_MISS"])
            foul = int(bucket["FOUL"])
            called_strike = int(bucket["CALLED_STRIKE"])
            ball = int(bucket["BALL"])

            rows.append(
                {
                    "Player": player_name,
                    "Count": count,
                    "BIP %": _pct(bip, pa),
                    "Swing and Miss %": _pct(swing_miss, pa),
                    "Foul %": _pct(foul, pa),
                    "Called Strike %": _pct(called_strike, pa),
                    "Ball %": _pct(ball, pa),
                    "Total PA": pa,
                }
            )

    return rows


__all__ = [
    "build_swing_decision_rows",
]