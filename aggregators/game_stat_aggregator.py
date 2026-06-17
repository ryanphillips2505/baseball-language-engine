from __future__ import annotations

from models.game import Game
from models.types import EventType


def _empty_player_stats() -> dict[str, int]:
    return {
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
        "GB": 0,
        "FB": 0,
        "BUNT": 0,
    }


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

            if pa.ball_type == "GB":
                stats[player]["GB"] += 1

            elif pa.ball_type == "FB":
                stats[player]["FB"] += 1

            elif pa.ball_type == "BUNT":
                stats[player]["BUNT"] += 1

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