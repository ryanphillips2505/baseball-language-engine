from __future__ import annotations


HITTING_KEYS = [
    "GP",
    "K",
    "BB",
    "HBP",
    "2B",
    "3B",
    "HR",
    "XBH",
    "XBH_LF",
    "XBH_CF",
    "XBH_RF",
    "XBH_UNKNOWN",
    "SB",
    "CS",
    "BIP",
    "GB",
    "FB",
    "BUNT",
]

LOCATION_KEYS = [
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

COMBO_KEYS = [
    f"{ball_type}-{location}"
    for ball_type in ["GB", "FB", "BUNT"]
    for location in LOCATION_KEYS
]


def build_season_summary_rows(
    opponent_iq_stats: dict[str, dict[str, dict[str, int]]],
) -> list[dict[str, int | str | float]]:
    rows: list[dict[str, int | str | float]] = []

    for player, sections in sorted(opponent_iq_stats.items()):
        hitting = sections["hitting"]
        locations = sections["locations"]
        combos = sections["combos"]

        row: dict[str, int | str | float] = {
            "Player": player,
        }

        for key in HITTING_KEYS:
            row[key] = hitting.get(key, 0)

        for key in LOCATION_KEYS:
            row[key] = locations.get(key, 0)

        for key in COMBO_KEYS:
            row[key] = combos.get(key, 0)

        bip = int(row.get("BIP", 0))
        gb = int(row.get("GB", 0))
        fb = int(row.get("FB", 0))

        row["GB%"] = (gb / bip) if bip else 0.0
        row["FB%"] = (fb / bip) if bip else 0.0

        rows.append(row)

    return rows