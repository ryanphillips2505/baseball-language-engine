from __future__ import annotations


GAME_STAT_KEYS = [
    "GP",
    "K",
    "BB",
    "HBP",
    "2B",
    "3B",
    "HR",
    "XBH",
    "SB",
    "CS",
    "BIP",
    "GB",
    "FB",
    "BUNT",
    "LOC_LF",
    "LOC_CF",
    "LOC_RF",
    "LOC_3B",
    "LOC_SS",
    "LOC_2B",
    "LOC_1B",
    "LOC_P",
    "XBH_LF",
    "XBH_CF",
    "XBH_RF",
    "XBH_UNKNOWN",
]


def _safe_int(value: object) -> int:
    try:
        return int(value or 0)
    except Exception:
        return 0


def build_player_card(
    player_name: str,
    game_stats: dict[str, dict[str, int]],
    swing_stats: dict[str, dict[str, dict[str, int]]] | None = None,
) -> dict[str, object]:
    player = str(player_name or "").strip()

    stats = game_stats.get(player, {}) if game_stats else {}
    swing = (swing_stats or {}).get(player, {})

    card = {
        "Player": player,
        "Season Summary": {},
        "Spray Zone": {},
        "Damage": {},
        "Swing Decision": swing,
    }

    for key in [
        "GP",
        "K",
        "BB",
        "HBP",
        "2B",
        "3B",
        "HR",
        "XBH",
        "SB",
        "CS",
        "BIP",
    ]:
        card["Season Summary"][key] = _safe_int(stats.get(key, 0))

    for key in [
        "LOC_LF",
        "LOC_CF",
        "LOC_RF",
        "LOC_3B",
        "LOC_SS",
        "LOC_2B",
        "LOC_1B",
        "LOC_P",
        "GB",
        "FB",
        "BUNT",
    ]:
        card["Spray Zone"][key] = _safe_int(stats.get(key, 0))

    for key in [
        "XBH",
        "XBH_LF",
        "XBH_CF",
        "XBH_RF",
        "XBH_UNKNOWN",
    ]:
        card["Damage"][key] = _safe_int(stats.get(key, 0))

    return card


def build_player_cards(
    game_stats: dict[str, dict[str, int]],
    swing_stats: dict[str, dict[str, dict[str, int]]] | None = None,
) -> list[dict[str, object]]:
    cards = []

    for player in sorted((game_stats or {}).keys()):
        player_name = str(player or "").strip()
        if not player_name:
            continue

        cards.append(
            build_player_card(
                player_name=player_name,
                game_stats=game_stats,
                swing_stats=swing_stats,
            )
        )

    return cards


__all__ = [
    "build_player_card",
    "build_player_cards",
]