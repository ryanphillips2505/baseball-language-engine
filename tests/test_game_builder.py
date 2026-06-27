from assemblers.game_builder import build_game
from models.game import Game


def test_build_game_builds_game_from_plate_appearance_blocks():
    pa_blocks = [
        "John Smith singles on a line drive to center fielder.",
        "Mike Jones strikes out swinging.",
    ]

    game = build_game(pa_blocks)

    assert isinstance(game, Game)
    assert len(game.plate_appearances) == 2
    assert game.plate_appearances[0].batter_name == "John Smith"
    assert game.plate_appearances[1].batter_name == "Mike Jones"