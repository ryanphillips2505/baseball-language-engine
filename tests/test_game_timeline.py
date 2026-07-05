from models.game import Game
from models.timeline import Timeline


def test_game_has_additive_empty_timeline_by_default():
    game = Game()

    assert hasattr(game, "plate_appearances")
    assert hasattr(game, "timeline")
    assert isinstance(game.timeline, Timeline)
    assert len(game.timeline) == 0
    assert game.plate_appearances == []


def test_game_timeline_does_not_share_state_between_games():
    game_one = Game()
    game_two = Game()

    assert game_one.timeline is not game_two.timeline
