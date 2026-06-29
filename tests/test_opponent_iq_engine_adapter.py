from adapters.opponent_iq_engine_adapter import (
    process_raw_text_to_opponent_iq_game,
    process_raw_text_to_opponent_iq_stats,
)


def test_process_raw_text_to_opponent_iq_stats():
    raw_text = """
    All Plays
    Top 1st
    John Smith singles on a line drive to center fielder.
    """

    stats = process_raw_text_to_opponent_iq_stats(raw_text)

    assert "John Smith" in stats
    assert stats["John Smith"]["BIP"] == 1
    assert stats["John Smith"]["CF"] == 1


def test_process_raw_text_to_opponent_iq_game_returns_legacy_contract():
    raw_text = """
    All Plays
    Top 1st
    John Smith singles on a line drive to center fielder.
    """

    game_team, game_players = process_raw_text_to_opponent_iq_game(raw_text)

    assert "John Smith" in game_players
    assert game_players["John Smith"]["BIP"] == 1
    assert game_players["John Smith"]["CF"] == 1

    assert game_team["BIP"] == 1
    assert game_team["CF"] == 1
