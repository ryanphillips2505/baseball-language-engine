from __future__ import annotations


TOP_LEVEL_LOCATION_OUTPUT_MAP = {
    "LOC_LF": "LF",
    "LOC_CF": "CF",
    "LOC_RF": "RF",
    "LOC_SS": "SS",
    "LOC_1B": "1B",
    "LOC_P": "P",
    "LOC_C": "C",
}

COMBO_LOCATION_OUTPUT_MAP = {
    "LOC_LF": "LF",
    "LOC_CF": "CF",
    "LOC_RF": "RF",
    "LOC_3B": "3B",
    "LOC_SS": "SS",
    "LOC_2B": "2B",
    "LOC_1B": "1B",
    "LOC_P": "P",
    "LOC_C": "C",
}

BALLTYPE_KEYS = [
    "GB",
    "FB",
    "BUNT",
]

HITTING_KEYS = [
    "GP",
    "K",
    "BB",
    "HBP",
    "1B",
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
    "RBI",
    "R",
]


def adapt_player_stats_to_opponent_iq(
    player_stats: dict[str, int],
) -> dict[str, int]:
    """
    Convert Baseball Language Engine internal player stats into
    one flat Opponent IQ-compatible player stat dict.
    """

    player_stats = player_stats or {}

    hitting = {}

    for key in HITTING_KEYS:
        hitting[key] = player_stats.get(key, 0)

    # Legacy Opponent IQ overloads these keys:
    # 2B = doubles + balls hit to second base
    # 3B = triples + balls hit to third base
    hitting["2B"] = player_stats.get("2B", 0) + player_stats.get("LOC_2B", 0)
    hitting["3B"] = player_stats.get("3B", 0) + player_stats.get("LOC_3B", 0)

    locations = {}

    for internal_key, output_key in TOP_LEVEL_LOCATION_OUTPUT_MAP.items():
        locations[output_key] = player_stats.get(internal_key, 0)

    combos = {}

    for ball_type in BALLTYPE_KEYS:
        for internal_location_key, output_location_key in COMBO_LOCATION_OUTPUT_MAP.items():
            internal_combo_key = f"{ball_type}-{internal_location_key}"
            output_combo_key = f"{ball_type}-{output_location_key}"

            combos[output_combo_key] = player_stats.get(internal_combo_key, 0)

    return {
        **hitting,
        **locations,
        **combos,
    }


def adapt_game_stats_to_opponent_iq(
    game_stats: dict[str, dict[str, int]],
) -> dict[str, dict[str, int]]:
    """
    Convert all player stats into Opponent IQ-compatible flat output shape.
    """

    return {
        player: adapt_player_stats_to_opponent_iq(player_stats)
        for player, player_stats in (game_stats or {}).items()
    }