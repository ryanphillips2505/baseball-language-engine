from __future__ import annotations

import pandas as pd


DAMAGE_COLUMNS = [
    "Player",
    "GP",
    "XBH_LF",
    "XBH_CF",
    "XBH_RF",
    "XBH",
]


def _to_int(value) -> int:
    try:
        if value is None or value == "":
            return 0
        return int(value)
    except Exception:
        try:
            return int(float(value))
        except Exception:
            return 0


def build_damage_dataframe(
    season_summary_rows: list[dict],
    active_players: list[str] | None = None,
) -> pd.DataFrame:
    active_set = set(active_players or [])

    rows = []

    for source_row in season_summary_rows:
        player = str(source_row.get("Player", "")).strip()

        if not player:
            continue

        if active_set and player not in active_set:
            continue

        xbh_lf = _to_int(source_row.get("XBH_LF", 0))
        xbh_cf = _to_int(source_row.get("XBH_CF", 0))
        xbh_rf = _to_int(source_row.get("XBH_RF", 0))

        rows.append(
            {
                "Player": player,
                "GP": _to_int(source_row.get("GP", 0)),
                "XBH_LF": xbh_lf,
                "XBH_CF": xbh_cf,
                "XBH_RF": xbh_rf,
                "XBH": xbh_lf + xbh_cf + xbh_rf,
            }
        )

    if not rows:
        return pd.DataFrame(columns=DAMAGE_COLUMNS)

    df = pd.DataFrame(rows).fillna(0)

    for column in DAMAGE_COLUMNS:
        if column not in df.columns:
            df[column] = 0

    df = df[DAMAGE_COLUMNS]
    df = df.sort_values("Player", kind="stable").reset_index(drop=True)

    return df