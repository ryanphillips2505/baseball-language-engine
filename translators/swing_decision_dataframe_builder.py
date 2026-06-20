from __future__ import annotations

import pandas as pd

from aggregators.swing_decision_aggregator import COUNT_ORDER
from translators.swing_decision_translator import build_swing_decision_rows


def _blank_row() -> dict[str, object]:
    return {
        "Count": "",
        "BIP %": "",
        "Swing and Miss %": "",
        "Foul %": "",
        "Called Strike %": "",
        "Ball %": "",
        "Total PA": "",
    }


def _header_row(label: str) -> dict[str, object]:
    return {
        "Count": label,
        "BIP %": "",
        "Swing and Miss %": "",
        "Foul %": "",
        "Called Strike %": "",
        "Ball %": "",
        "Total PA": "",
    }


def build_swing_decision_dataframe(
    swing_stats: dict[str, dict[str, dict[str, int]]],
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []

    team_totals = {
        count: {
            "PA": 0,
            "BIP": 0,
            "SWING_MISS": 0,
            "FOUL": 0,
            "CALLED_STRIKE": 0,
            "BALL": 0,
        }
        for count in COUNT_ORDER
    }

    for player_counts in swing_stats.values():
        for count in COUNT_ORDER:
            bucket = player_counts[count]
            team_totals[count]["PA"] += int(bucket["PA"])
            team_totals[count]["BIP"] += int(bucket["BIP"])
            team_totals[count]["SWING_MISS"] += int(bucket["SWING_MISS"])
            team_totals[count]["FOUL"] += int(bucket["FOUL"])
            team_totals[count]["CALLED_STRIKE"] += int(bucket["CALLED_STRIKE"])
            team_totals[count]["BALL"] += int(bucket["BALL"])

    rows.append(_header_row("TEAM TOTAL"))

    team_rows = build_swing_decision_rows({"TEAM TOTAL": team_totals})
    for row in team_rows:
        rows.append(
            {
                "Count": row["Count"],
                "BIP %": row["BIP %"],
                "Swing and Miss %": row["Swing and Miss %"],
                "Foul %": row["Foul %"],
                "Called Strike %": row["Called Strike %"],
                "Ball %": row["Ball %"],
                "Total PA": row["Total PA"],
            }
        )

    rows.append(_blank_row())

    player_order = sorted(
        swing_stats.keys(),
        key=lambda player: (
            -int(swing_stats[player]["0-0"]["PA"]),
            str(player).lower(),
        ),
    )

    for player_name in player_order:
        rows.append(_header_row(player_name))

        player_rows = build_swing_decision_rows(
            {player_name: swing_stats[player_name]}
        )

        for row in player_rows:
            rows.append(
                {
                    "Count": row["Count"],
                    "BIP %": row["BIP %"],
                    "Swing and Miss %": row["Swing and Miss %"],
                    "Foul %": row["Foul %"],
                    "Called Strike %": row["Called Strike %"],
                    "Ball %": row["Ball %"],
                    "Total PA": row["Total PA"],
                }
            )

        rows.append(_blank_row())

    return pd.DataFrame(
        rows,
        columns=[
            "Count",
            "BIP %",
            "Swing and Miss %",
            "Foul %",
            "Called Strike %",
            "Ball %",
            "Total PA",
        ],
    )


__all__ = [
    "build_swing_decision_dataframe",
]