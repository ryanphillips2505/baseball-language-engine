from __future__ import annotations


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


def build_spray_zone_rows(
    season_summary_rows: list[dict],
) -> list[dict[str, int | str]]:
    rows: list[dict[str, int | str]] = []

    for source_row in season_summary_rows:
        player = str(source_row.get("Player", "")).strip()

        if not player:
            continue

        lf = _to_int(source_row.get("GB-LF", 0)) + _to_int(source_row.get("FB-LF", 0))
        cf = _to_int(source_row.get("GB-CF", 0)) + _to_int(source_row.get("FB-CF", 0))
        rf = _to_int(source_row.get("GB-RF", 0)) + _to_int(source_row.get("FB-RF", 0))

        left_infield = (
            _to_int(source_row.get("GB-3B", 0))
            + _to_int(source_row.get("FB-3B", 0))
            + _to_int(source_row.get("GB-SS", 0))
            + _to_int(source_row.get("FB-SS", 0))
        )

        right_infield = (
            _to_int(source_row.get("GB-2B", 0))
            + _to_int(source_row.get("FB-2B", 0))
            + _to_int(source_row.get("GB-1B", 0))
            + _to_int(source_row.get("FB-1B", 0))
        )

        bip = lf + cf + rf + left_infield + right_infield

        rows.append(
            {
                "Player": player,
                "LF": lf,
                "CF": cf,
                "RF": rf,
                "3B/SS": left_infield,
                "2B/1B": right_infield,
                "BIP": bip,
            }
        )

    return rows