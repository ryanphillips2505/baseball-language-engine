from __future__ import annotations

import pandas as pd


SPRAY_ZONE_COLUMNS = [
    "Player",
    "LF",
    "CF",
    "RF",
    "3B/SS",
    "2B/1B",
    "BIP",
]


def build_spray_zone_dataframe(
    spray_zone_rows: list[dict],
) -> pd.DataFrame:
    if not spray_zone_rows:
        return pd.DataFrame(columns=SPRAY_ZONE_COLUMNS)

    df = pd.DataFrame(spray_zone_rows).fillna(0)

    for column in SPRAY_ZONE_COLUMNS:
        if column not in df.columns:
            df[column] = 0

    df = df[SPRAY_ZONE_COLUMNS]
    df = df.sort_values("Player", kind="stable").reset_index(drop=True)

    return df