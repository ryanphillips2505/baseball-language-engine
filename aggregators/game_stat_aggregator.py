from __future__ import annotations

from models.game import Game
from models.types import EventType


RAW_LOCATION_KEYS = [
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

LOCATION_KEY_MAP = {
    "LF": "LOC_LF",
    "CF": "LOC_CF",
    "RF": "LOC_RF",
    "3B": "LOC_3B",
    "SS": "LOC_SS",
    "2B": "LOC_2B",
    "1B": "LOC_1B",
    "P": "LOC_P",
    "C": "LOC_C",
}

LOCATION_KEYS = list(LOCATION_KEY_MAP.values())

BALLTYPE_KEYS = [
    "GB",
    "FB",
    "BUNT",
    
]

XBH_LOCATION_KEYS = [
    "XBH_LF",
    "XBH_CF",
    "XBH_RF",
    "XBH_UNKNOWN",
]

COMBO_KEYS = [
    f"{ball_type}-{location_key}"
    for ball_type in BALLTYPE_KEYS
    for location_key in LOCATION_KEYS
]


def _empty_player_stats() -> dict[str, int]:
    stats = {
        "GP": 1,
        "K": 0,
        "BB": 0,
        "HBP": 0,
        "2B": 0,
        "3B": 0,
        "HR": 0,
        "XBH": 0,
        "SB": 0,
        "CS": 0,
        "BIP": 0,
    }

    for location_key in LOCATION_KEYS:
        stats[location_key] = 0

    for ball_type in BALLTYPE_KEYS:
        stats[ball_type] = 0

    for combo_key in COMBO_KEYS:
        stats[combo_key] = 0
    
    for xbh_location_key in XBH_LOCATION_KEYS:
        stats[xbh_location_key] = 0

    return stats


def _location_stat_key(raw_location: str | None) -> str | None:
    if raw_location is None:
        return None

    return LOCATION_KEY_MAP.get(raw_location)


def aggregate_game_stats(game: Game) -> dict[str, dict[str, int]]:
    """
    Convert a Game object into player stat totals.

    Important:
    Hit result keys use traditional baseball names:
    - 2B = double
    - 3B = triple

    Field location keys are stored internally with LOC_ prefixes:
    - LOC_2B = ball hit to second-base area
    - LOC_3B = ball hit to third-base area

    This prevents collisions while still allowing the report layer to display
    Opponent IQ-style labels later.
    """

    stats: dict[str, dict[str, int]] = {}

    for player in game.players_in_game():
        stats[player] = _empty_player_stats()

    for pa in game.plate_appearances:
        if pa.batter_name:
            player = pa.batter_name

            if player not in stats:
                stats[player] = _empty_player_stats()

            location_key = _location_stat_key(pa.location)

            if pa.is_bip:
                stats[player]["BIP"] += 1

            if location_key:
                stats[player][location_key] += 1

            if pa.ball_type in BALLTYPE_KEYS:
                stats[player][pa.ball_type] += 1

            if pa.ball_type in BALLTYPE_KEYS and location_key:
                combo_key = f"{pa.ball_type}-{location_key}"
                stats[player][combo_key] += 1

            if pa.baseball_event:
                event = pa.baseball_event.primary_event

                if event in {
                    EventType.STRIKEOUT_LOOKING,
                    EventType.STRIKEOUT_SWINGING,
                    EventType.DROPPED_THIRD_STRIKE_REACH,
                    EventType.DROPPED_THIRD_STRIKE_OUT,
                }:
                    stats[player]["K"] += 1

                elif event == EventType.WALK:
                    stats[player]["BB"] += 1

                elif event == EventType.HIT_BY_PITCH:
                    stats[player]["HBP"] += 1

                elif event == EventType.DOUBLE:
                    stats[player]["2B"] += 1

                elif event == EventType.TRIPLE:
                    stats[player]["3B"] += 1

                elif event == EventType.HOME_RUN:
                    stats[player]["HR"] += 1

                if event in {
                    EventType.DOUBLE,
                    EventType.TRIPLE,
                    EventType.HOME_RUN,
                }:
                    stats[player]["XBH"] += 1

                    if pa.location in {"LF", "CF", "RF"}:
                        stats[player][f"XBH_{pa.location}"] += 1
                    else:
                        stats[player]["XBH_UNKNOWN"] += 1

        for runner_event in pa.runner_events:
            if not runner_event.runner_name:
                continue

            player = runner_event.runner_name

            if player not in stats:
                stats[player] = _empty_player_stats()

            if runner_event.event_type == "SB":
                stats[player]["SB"] += 1

            elif runner_event.event_type == "CS":
                stats[player]["CS"] += 1

    return stats