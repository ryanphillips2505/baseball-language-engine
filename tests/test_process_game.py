from models.game import Game
from pipeline.process_game import process_game


def test_process_game_returns_game_from_gamechanger_text():
    raw_text = """
    All Plays
    Top 1st
    John Smith singles on a line drive to center fielder.
    """

    game = process_game(raw_text)

    assert isinstance(game, Game)
    assert len(game.plate_appearances) >= 1