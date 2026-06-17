from aggregators.game_stat_aggregator import aggregate_game_stats
from models.baseball_event import BaseballEvent
from models.game import Game
from models.plate_appearance import PlateAppearance
from models.types import EventType


def test_aggregate_game_stats_tracks_gp():
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

    stats = aggregate_game_stats(game)

    assert stats["John Smith"]["GP"] == 1
