from __future__ import annotations

from models.game import Game
from models.types import EventType


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

BALLTYPE_KEYS = [
    "GB",
    "FB",
    "BUNT",
]

COMBO_KEYS = [
    f"{ball_type}-{location}"
    for ball_type in BALLTYPE_KEYS
    for location in LOCATION_KEYS
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

    for location in LOCATION_KEYS:
        stats[location] = 0

    for ball_type in BALLTYPE_KEYS:
        stats[ball_type] = 0

    for combo_key in COMBO_KEYS:
        stats[combo_key] = 0

    return stats


def aggregate_game_stats(game: Game) -> dict[str, dict[str, int]]:
    """
    Convert a Game object into player stat totals.
    """

    stats: dict[str, dict[str, int]] = {}

    for player in game.players_in_game():
        stats[player] = _empty_player_stats()

    for pa in game.plate_appearances:
        if pa.batter_name:
            player = pa.batter_name

            if player not in stats:
                stats[player] = _empty_player_stats()

            if pa.is_bip:
                stats[player]["BIP"] += 1

            if pa.location in LOCATION_KEYS:
                stats[player][pa.location] += 1

            if pa.ball_type in BALLTYPE_KEYS:
                stats[player][pa.ball_type] += 1

            if pa.ball_type in BALLTYPE_KEYS and pa.location in LOCATION_KEYS:
                combo_key = f"{pa.ball_type}-{pa.location}"
                stats[player][combo_key] += 1

            if pa.baseball_event:
                event = pa.baseball_event.primary_event

                if event in {
                    EventType.STRIKEOUT_LOOKING,
                    EventType.STRIKEOUT_SWINGING,
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