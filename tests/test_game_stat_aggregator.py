from aggregators.game_stat_aggregator import aggregate_game_stats
from models.baseball_event import BaseballEvent
from models.game import Game
from models.plate_appearance import PlateAppearance
from models.types import EventType
from models.runner_event import RunnerEvent


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


def test_aggregate_game_stats_tracks_strikeout():
    game = Game(
        plate_appearances=[
            PlateAppearance(
                batter_name="John Smith",
                baseball_event=BaseballEvent(
                    primary_event=EventType.STRIKEOUT_SWINGING,
                    secondary_events=[],
                ),
            )
        ]
    )

    stats = aggregate_game_stats(game)

    assert stats["John Smith"]["K"] == 1


def test_aggregate_game_stats_tracks_walk():
    game = Game(
        plate_appearances=[
            PlateAppearance(
                batter_name="John Smith",
                baseball_event=BaseballEvent(
                    primary_event=EventType.WALK,
                    secondary_events=[],
                ),
            )
        ]
    )

    stats = aggregate_game_stats(game)

    assert stats["John Smith"]["BB"] == 1


def test_aggregate_game_stats_tracks_hbp():
    game = Game(
        plate_appearances=[
            PlateAppearance(
                batter_name="John Smith",
                baseball_event=BaseballEvent(
                    primary_event=EventType.HIT_BY_PITCH,
                    secondary_events=[],
                ),
            )
        ]
    )

    stats = aggregate_game_stats(game)

    assert stats["John Smith"]["HBP"] == 1


def test_aggregate_game_stats_tracks_double():
    game = Game(
        plate_appearances=[
            PlateAppearance(
                batter_name="John Smith",
                baseball_event=BaseballEvent(
                    primary_event=EventType.DOUBLE,
                    secondary_events=[],
                ),
            )
        ]
    )

    stats = aggregate_game_stats(game)

    assert stats["John Smith"]["2B"] == 1


def test_aggregate_game_stats_tracks_triple():
    game = Game(
        plate_appearances=[
            PlateAppearance(
                batter_name="John Smith",
                baseball_event=BaseballEvent(
                    primary_event=EventType.TRIPLE,
                    secondary_events=[],
                ),
            )
        ]
    )

    stats = aggregate_game_stats(game)

    assert stats["John Smith"]["3B"] == 1


def test_aggregate_game_stats_tracks_home_run():
    game = Game(
        plate_appearances=[
            PlateAppearance(
                batter_name="John Smith",
                baseball_event=BaseballEvent(
                    primary_event=EventType.HOME_RUN,
                    secondary_events=[],
                ),
            )
        ]
    )

    stats = aggregate_game_stats(game)

    assert stats["John Smith"]["HR"] == 1

def test_aggregate_game_stats_tracks_xbh_from_double():
    game = Game(
        plate_appearances=[
            PlateAppearance(
                batter_name="John Smith",
                baseball_event=BaseballEvent(
                    primary_event=EventType.DOUBLE,
                    secondary_events=[],
                ),
            )
        ]
    )

    stats = aggregate_game_stats(game)

    assert stats["John Smith"]["XBH"] == 1


def test_aggregate_game_stats_tracks_xbh_from_triple():
    game = Game(
        plate_appearances=[
            PlateAppearance(
                batter_name="John Smith",
                baseball_event=BaseballEvent(
                    primary_event=EventType.TRIPLE,
                    secondary_events=[],
                ),
            )
        ]
    )

    stats = aggregate_game_stats(game)

    assert stats["John Smith"]["XBH"] == 1


def test_aggregate_game_stats_tracks_xbh_from_home_run():
    game = Game(
        plate_appearances=[
            PlateAppearance(
                batter_name="John Smith",
                baseball_event=BaseballEvent(
                    primary_event=EventType.HOME_RUN,
                    secondary_events=[],
                ),
            )
        ]
    )

    stats = aggregate_game_stats(game)

    assert stats["John Smith"]["XBH"] == 1

def test_aggregate_game_stats_tracks_stolen_base():
    game = Game(
        plate_appearances=[
            PlateAppearance(
                batter_name=None,
                baseball_event=None,
                runner_events=[
                    RunnerEvent(
                        event_type="SB",
                        base="2B",
                        runner_name="John Smith",
                    )
                ],
            )
        ]
    )

    stats = aggregate_game_stats(game)

    assert stats["John Smith"]["SB"] == 1


def test_aggregate_game_stats_tracks_caught_stealing():
    game = Game(
        plate_appearances=[
            PlateAppearance(
                batter_name=None,
                baseball_event=None,
                runner_events=[
                    RunnerEvent(
                        event_type="CS",
                        base="2B",
                        runner_name="John Smith",
                    )
                ],
            )
        ]
    )

    stats = aggregate_game_stats(game)

    assert stats["John Smith"]["CS"] == 1

def test_aggregate_game_stats_tracks_bip():
    game = Game(
        plate_appearances=[
            PlateAppearance(
                batter_name="John Smith",
                baseball_event=None,
                is_bip=True,
            )
        ]
    )

    stats = aggregate_game_stats(game)

    assert stats["John Smith"]["BIP"] == 1


def test_aggregate_game_stats_tracks_ground_ball():
    game = Game(
        plate_appearances=[
            PlateAppearance(
                batter_name="John Smith",
                baseball_event=None,
                is_bip=True,
                ball_type="GB",
            )
        ]
    )

    stats = aggregate_game_stats(game)

    assert stats["John Smith"]["GB"] == 1


def test_aggregate_game_stats_tracks_fly_ball():
    game = Game(
        plate_appearances=[
            PlateAppearance(
                batter_name="John Smith",
                baseball_event=None,
                is_bip=True,
                ball_type="FB",
            )
        ]
    )

    stats = aggregate_game_stats(game)

    assert stats["John Smith"]["FB"] == 1


def test_aggregate_game_stats_tracks_bunt():
    game = Game(
        plate_appearances=[
            PlateAppearance(
                batter_name="John Smith",
                baseball_event=None,
                is_bip=True,
                ball_type="BUNT",
            )
        ]
    )
def test_aggregate_game_stats_tracks_location():
    game = Game(
        plate_appearances=[
            PlateAppearance(
                batter_name="John Smith",
                baseball_event=None,
                is_bip=True,
                location="RF",
            )
        ]
    )

    stats = aggregate_game_stats(game)

    assert stats["John Smith"]["RF"] == 1


def test_aggregate_game_stats_tracks_gb_location_combo():
    game = Game(
        plate_appearances=[
            PlateAppearance(
                batter_name="John Smith",
                baseball_event=None,
                is_bip=True,
                ball_type="GB",
                location="SS",
            )
        ]
    )

    stats = aggregate_game_stats(game)

    assert stats["John Smith"]["GB"] == 1
    assert stats["John Smith"]["SS"] == 1
    assert stats["John Smith"]["GB-SS"] == 1


def test_aggregate_game_stats_tracks_fb_location_combo():
    game = Game(
        plate_appearances=[
            PlateAppearance(
                batter_name="John Smith",
                baseball_event=None,
                is_bip=True,
                ball_type="FB",
                location="CF",
            )
        ]
    )

    stats = aggregate_game_stats(game)

    assert stats["John Smith"]["FB"] == 1
    assert stats["John Smith"]["CF"] == 1
    assert stats["John Smith"]["FB-CF"] == 1


def test_aggregate_game_stats_tracks_bunt_location_combo():
    game = Game(
        plate_appearances=[
            PlateAppearance(
                batter_name="John Smith",
                baseball_event=None,
                is_bip=True,
                ball_type="BUNT",
                location="3B",
            )
        ]
    )

    stats = aggregate_game_stats(game)

    assert stats["John Smith"]["BUNT"] == 1
    assert stats["John Smith"]["3B"] == 1
    assert stats["John Smith"]["BUNT-3B"] == 1


    stats = aggregate_game_stats(game)

    assert stats["John Smith"]["BUNT"] == 1
