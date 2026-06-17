from aggregators.game_stat_aggregator import aggregate_game_stats
from assemblers.plate_appearance_builder import build_plate_appearance
from models.game import Game


def test_real_gc_parity_sample():
    game = Game(
        plate_appearances=[
            build_plate_appearance(
                "Wyatt Jones singles on a bunt to third baseman Thatcher Jack."
            ),
            build_plate_appearance(
                "Gentry Hoke strikes out swinging, Caleb Adams pitching, Wyatt Jones remains at 1st."
            ),
            build_plate_appearance(
                "Preston Klose grounds out to shortstop Ethan Vinson."
            ),
            build_plate_appearance(
                "Wyatt Jones caught stealing 2nd, second baseman Julio Alonso Gutierrez."
            ),
        ]
    )

    stats = aggregate_game_stats(game)

    # Wyatt Jones

    assert stats["Wyatt Jones"]["GP"] == 1
    assert stats["Wyatt Jones"]["CS"] == 1

    # Gentry Hoke

    assert stats["Gentry Hoke"]["GP"] == 1
    assert stats["Gentry Hoke"]["K"] == 1

    # Preston Klose

    assert stats["Preston Klose"]["GP"] == 1
    assert stats["Preston Klose"]["BIP"] == 1
    assert stats["Preston Klose"]["GB"] == 1
    assert stats["Preston Klose"]["SS"] == 1
    assert stats["Preston Klose"]["GB-SS"] == 1