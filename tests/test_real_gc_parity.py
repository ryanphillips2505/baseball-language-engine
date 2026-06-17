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
    assert stats["Preston Klose"]["LOC_SS"] == 1
    assert stats["Preston Klose"]["GB-LOC_SS"] == 1

def test_real_gc_third_inning_parity():
    game = Game(
        plate_appearances=[
            build_plate_appearance(
                "Owen Blair hits a ground ball and reaches on an error by second baseman Julio Alonso Gutierrez."
            ),
            build_plate_appearance(
                "Caleb Schneider walks, Caleb Adams pitching, Wyatt Ruzicka advances to 2nd."
            ),
            build_plate_appearance(
                "Cade Geiger out on infield fly to shortstop Ethan Vinson, Wyatt Ruzicka remains at 2nd, Caleb Schneider remains at 1st."
            ),
            build_plate_appearance(
                "Zayden Khalil walks, Caleb Adams pitching, Wyatt Ruzicka advances to 3rd, Caleb Schneider advances to 2nd."
            ),
            build_plate_appearance(
                "Eddie Fish walks, Caleb Adams pitching, Wyatt Ruzicka scores, Caleb Schneider advances to 3rd, Zayden Khalil advances to 2nd."
            ),
            build_plate_appearance(
                "Drake Pace doubles on a line drive to right fielder Ryan Barfield, Caleb Schneider scores, Zayden Khalil scores, Eddie Fish advances to 3rd."
            ),
            build_plate_appearance(
                "Wyatt Jones strikes out looking, Caleb Adams pitching."
            ),
        ]
    )

    stats = aggregate_game_stats(game)

    assert stats["Owen Blair"]["GP"] == 1

    assert stats["Caleb Schneider"]["GP"] == 1
    assert stats["Caleb Schneider"]["BB"] == 1

    assert stats["Cade Geiger"]["GP"] == 1
    assert stats["Cade Geiger"]["BIP"] == 1

    assert stats["Zayden Khalil"]["GP"] == 1
    assert stats["Zayden Khalil"]["BB"] == 1

    assert stats["Eddie Fish"]["GP"] == 1
    assert stats["Eddie Fish"]["BB"] == 1

    assert stats["Drake Pace"]["GP"] == 1
    assert stats["Drake Pace"]["2B"] == 1
    assert stats["Drake Pace"]["XBH"] == 1

    assert stats["Wyatt Jones"]["GP"] == 1
    assert stats["Wyatt Jones"]["K"] == 1