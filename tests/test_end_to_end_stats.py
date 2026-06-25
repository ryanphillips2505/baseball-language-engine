from aggregators.game_stat_aggregator import aggregate_game_stats
from cleaners.gamechanger_cleaner import clean_gamechanger_text
from assemblers.plate_appearance_builder import build_plate_appearance
from models.game import Game


def test_end_to_end_stats_from_baseball_language():
    game = Game(
        plate_appearances=[
            build_plate_appearance(
                "John Smith doubled to right field."
            ),
            build_plate_appearance(
                "John Smith homered to left field."
            ),
            build_plate_appearance(
                "John Smith struck out swinging."
            ),
            build_plate_appearance(
                "John Smith walks."
            ),
            build_plate_appearance(
                "Mike Brown steals third base."
            ),
        ]
    )

    stats = aggregate_game_stats(game)

    assert stats["John Smith"]["GP"] == 1
    assert stats["John Smith"]["2B"] == 1
    assert stats["John Smith"]["HR"] == 1
    assert stats["John Smith"]["XBH"] == 2
    assert stats["John Smith"]["K"] == 1
    assert stats["John Smith"]["BB"] == 1

    assert stats["Mike Brown"]["GP"] == 1
    assert stats["Mike Brown"]["SB"] == 1