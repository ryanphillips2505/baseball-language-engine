from adapters.legacy_process_game_text import process_game_text


def test_legacy_process_game_text_returns_team_and_players():
    raw_text = """
    All Plays
    Top 1st
    John Smith singles on a line drive to center fielder.
    """

    game_team, game_players = process_game_text(raw_text)

    assert game_team["BIP"] == 1
    assert game_team["CF"] == 1

    assert "John Smith" in game_players
    assert game_players["John Smith"]["BIP"] == 1
    assert game_players["John Smith"]["CF"] == 1