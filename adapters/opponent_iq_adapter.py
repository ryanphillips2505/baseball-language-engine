from __future__ import annotations


LOCATION_OUTPUT_MAP = {
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
]


def adapt_player_stats_to_opponent_iq(
    player_stats: dict[str, int],
) -> dict[str, dict[str, int]]:
    """
    Convert Baseball Language Engine internal player stats into
    an Opponent IQ-compatible output shape.

    Important:
    The internal engine keeps location keys safe:

    LOC_2B = hit location to second-base area
    2B = double

    This adapter maps locations back to Opponent IQ display labels
    without overwriting hitting stats.
    """

    hitting = {}

    for key in HITTING_KEYS:
        hitting[key] = player_stats.get(key, 0)

    locations = {}

    for internal_key, output_key in LOCATION_OUTPUT_MAP.items():
        locations[output_key] = player_stats.get(internal_key, 0)

    combos = {}

    for ball_type in BALLTYPE_KEYS:
        for internal_location_key, output_location_key in LOCATION_OUTPUT_MAP.items():
            internal_combo_key = f"{ball_type}-{internal_location_key}"
            output_combo_key = f"{ball_type}-{output_location_key}"

            combos[output_combo_key] = player_stats.get(internal_combo_key, 0)

    return {
        "hitting": hitting,
        "locations": locations,
        "combos": combos,
    }


def adapt_game_stats_to_opponent_iq(
    game_stats: dict[str, dict[str, int]],
) -> dict[str, dict[str, dict[str, int]]]:
    """
    Convert all player stats into Opponent IQ-compatible output shape.
    """

    return {
        player: adapt_player_stats_to_opponent_iq(player_stats)
        for player, player_stats in game_stats.items()
    }
