from __future__ import annotations

import pandas as pd


LOCATION_KEYS = ["P", "1B", "2B", "3B", "SS", "LF", "CF", "RF"]
RIGHT_STAT_KEYS = ["BUNT", "K", "BB", "SB", "CS"]


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


def build_season_summary_dataframe(
    season_summary_rows: list[dict],
    active_players: list[str] | None = None,
) -> pd.DataFrame:
    ordered_cols = [
        "Player",
        "GP",
        "GB%",
        "FB%",
        *[f"GB-{location}" for location in LOCATION_KEYS],
        *[f"FB-{location}" for location in LOCATION_KEYS],
        "BIP",
        *RIGHT_STAT_KEYS,
    ]

    if not season_summary_rows:
        return pd.DataFrame(columns=ordered_cols)

    active_set = set(active_players or [])

    rows = []

    for source_row in season_summary_rows:
        player = str(source_row.get("Player", "")).strip()

        if not player:
            continue

        if active_set and player not in active_set:
            continue

        gb_total = _to_int(source_row.get("GB", 0))
        fb_total = _to_int(source_row.get("FB", 0))
        bip_total = gb_total + fb_total

        row = {
            "Player": player,
            "GP": _to_int(source_row.get("GP", 0)),
            "GB%": (gb_total / bip_total) if bip_total > 0 else 0.0,
            "FB%": (fb_total / bip_total) if bip_total > 0 else 0.0,
        }

        for location in LOCATION_KEYS:
            gb_location = _to_int(source_row.get(f"GB-{location}", 0))
            fb_location = _to_int(source_row.get(f"FB-{location}", 0))

            row[f"GB-{location}"] = (
                gb_location / bip_total
                if bip_total > 0
                else 0.0
            )
            row[f"FB-{location}"] = (
                fb_location / bip_total
                if bip_total > 0
                else 0.0
            )

        row["BIP"] = bip_total

        for key in RIGHT_STAT_KEYS:
            row[key] = _to_int(source_row.get(key, 0))

        rows.append(row)

    if not rows:
        return pd.DataFrame(columns=ordered_cols)

    df = pd.DataFrame(rows).fillna(0)

    for column in ordered_cols:
        if column not in df.columns:
            df[column] = 0

    df = df[ordered_cols]
    df = df.sort_values("Player", kind="stable").reset_index(drop=True)

    return df