from __future__ import annotations

from models.game import Game


def aggregate_game_stats(game: Game) -> dict[str, dict[str, int]]:
    """
    Convert a Game object into player stat totals.

    Phase 9A starts intentionally small.
    """

    stats: dict[str, dict[str, int]] = {}

    for player in game.players_in_game():
        stats[player] = {
            "GP": 1,
        }

    return stats
