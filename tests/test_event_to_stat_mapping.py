from aggregators.game_stat_aggregator import aggregate_game_stats
from models.baseball_event import BaseballEvent
from models.game import Game
from models.plate_appearance import PlateAppearance
from models.types import EventType


def _build_game(event_type: EventType) -> Game:
    return Game(
        plate_appearances=[
            PlateAppearance(
                batter_name="John Smith",
                baseball_event=BaseballEvent(
                    primary_event=event_type,
                    secondary_events=[],
                ),
            )
        ]
    )


def test_double_maps_to_double_stat():
    stats = aggregate_game_stats(
        _build_game(EventType.DOUBLE)
    )

    assert stats["John Smith"]["2B"] == 1
    assert stats["John Smith"]["XBH"] == 1


def test_triple_maps_to_triple_stat():
    stats = aggregate_game_stats(
        _build_game(EventType.TRIPLE)
    )

    assert stats["John Smith"]["3B"] == 1
    assert stats["John Smith"]["XBH"] == 1


def test_home_run_maps_to_home_run_stat():
    stats = aggregate_game_stats(
        _build_game(EventType.HOME_RUN)
    )

    assert stats["John Smith"]["HR"] == 1
    assert stats["John Smith"]["XBH"] == 1


def test_walk_maps_to_bb_stat():
    stats = aggregate_game_stats(
        _build_game(EventType.WALK)
    )

    assert stats["John Smith"]["BB"] == 1


def test_hbp_maps_to_hbp_stat():
    stats = aggregate_game_stats(
        _build_game(EventType.HIT_BY_PITCH)
    )

    assert stats["John Smith"]["HBP"] == 1


def test_strikeout_swinging_maps_to_k_stat():
    stats = aggregate_game_stats(
        _build_game(EventType.STRIKEOUT_SWINGING)
    )

    assert stats["John Smith"]["K"] == 1


def test_strikeout_looking_maps_to_k_stat():
    stats = aggregate_game_stats(
        _build_game(EventType.STRIKEOUT_LOOKING)
    )

    assert stats["John Smith"]["K"] == 1