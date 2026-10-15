from __future__ import annotations

from adapters.opponent_iq_adapter import adapt_game_stats_to_opponent_iq
from aggregators.game_stat_aggregator import aggregate_game_stats
from language.names import resolve_player_stats
from pipeline.process_game import process_game


def _filter_players_by_roster(
    game_players: dict[str, dict[str, int]],
    roster_names: set[str] | None,
) -> dict[str, dict[str, int]]:
    if not roster_names:
        return game_players

    # Name recognition: "L. Devault", "Devault, L." and "Lawson DeVault"
    # all resolve to the roster's "Lawson DeVault". Exact spellings match
    # exactly as before; ambiguous names stay unmatched.
    filtered, _unmatched = resolve_player_stats(game_players, roster_names)

    return filtered


def process_game_text(
    raw_text: str,
    roster_names: set[str] | None = None,
) -> tuple[dict, dict]:
    """
    Compatibility adapter.

    Returns the same (game_team, game_players) structure that the
    legacy Opponent IQ parser returns today, but generated entirely
    by the Baseball Language Engine.
    """

    game = process_game(raw_text)

    game_stats = aggregate_game_stats(game)

    game_players = adapt_game_stats_to_opponent_iq(game_stats)

    game_players = _filter_players_by_roster(
        game_players,
        roster_names,
    )

    game_team: dict[str, int] = {}

    for player_stats in game_players.values():
        for key, value in player_stats.items():
            if key == "GP":
                continue

            game_team[key] = game_team.get(key, 0) + int(value)

    all_game_players = adapt_game_stats_to_opponent_iq(game_stats)

    game_team["SB"] = sum(
        int(player_stats.get("SB", 0))
        for player_stats in all_game_players.values()
    )

    game_team["CS"] = sum(
        int(player_stats.get("CS", 0))
        for player_stats in all_game_players.values()
    )

    return game_team, game_players


__all__ = [
    "process_game_text",
]