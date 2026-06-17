from __future__ import annotations

from models.game import Game
from models.types import EventType


def aggregate_game_stats(game: Game) -> dict[str, dict[str, int]]:
    """
    Convert a Game object into player stat totals.

    Phase 9A:
    GP
    K
    BB
    HBP
    """

    stats: dict[str, dict[str, int]] = {}

    for player in game.players_in_game():
        stats[player] = {
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
        }

    for pa in game.plate_appearances:
        if not pa.batter_name:
            continue

        if not pa.baseball_event:
            continue

        player = pa.batter_name
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
            stats[player] = {
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
            }

        if runner_event.event_type == "SB":
            stats[player]["SB"] += 1

        elif runner_event.event_type == "CS":
            stats[player]["CS"] += 1

    return stats