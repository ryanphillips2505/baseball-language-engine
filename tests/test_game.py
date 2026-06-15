from models.baseball_event import BaseballEvent
from models.game import Game
from models.plate_appearance import PlateAppearance
from models.runner_event import RunnerEvent
from models.types import EventType


def test_game_tracks_players_in_game_from_batters():
    game = Game(
        plate_appearances=[
            PlateAppearance(
                batter_name="John Smith",
                baseball_event=BaseballEvent(
                    primary_event=EventType.SINGLE,
                    secondary_events=[],
                ),
            )
        ]
    )

    assert game.players_in_game() == {"John Smith"}


def test_game_tracks_players_in_game_from_runner_events():
    game = Game(
        plate_appearances=[
            PlateAppearance(
                batter_name=None,
                baseball_event=None,
                runner_events=[
                    RunnerEvent(
                        event_type="SB",
                        base="2B",
                        runner_name="Mike Brown",
                    )
                ],
            )
        ]
    )

    assert game.players_in_game() == {"Mike Brown"}