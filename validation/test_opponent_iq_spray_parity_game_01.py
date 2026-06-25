from pathlib import Path

from aggregators.game_stat_aggregator import aggregate_game_stats
from assemblers.plate_appearance_builder import build_plate_appearance
from cleaners.gamechanger_cleaner import clean_gamechanger_text
from models.game import Game


SAMPLE_PATH = Path(
    "samples/gamechanger/risin_shockers_2026_06_04.txt"
)


def build_game(raw_text: str) -> Game:
    cleaned = clean_gamechanger_text(raw_text)

    return Game(
        plate_appearances=[
            build_plate_appearance(block)
            for block in cleaned
        ]
    )


...
def test_opponent_iq_spray_parity_game_01():
    raw_text = SAMPLE_PATH.read_text(encoding="utf-8")
    game = build_game(raw_text)
    stats = aggregate_game_stats(game)

    expected = {
        "Wade Webb": {
            "BIP": 3, "LOC_LF": 1, "LOC_CF": 2, "LOC_RF": 0,
            "LOC_3B": 0, "LOC_SS": 0, "LOC_2B": 0, "LOC_1B": 0,
            "LOC_P": 0, "GB": 0, "FB": 3, "BUNT": 0,
        },
        "Miles Stanley": {
            "BIP": 1, "LOC_LF": 1, "LOC_CF": 0, "LOC_RF": 0,
            "LOC_3B": 0, "LOC_SS": 0, "LOC_2B": 0, "LOC_1B": 0,
            "LOC_P": 0, "GB": 0, "FB": 1, "BUNT": 0,
        },
        "Traylon Barnes": {
            "BIP": 1, "LOC_LF": 1, "LOC_CF": 0, "LOC_RF": 0,
            "LOC_3B": 0, "LOC_SS": 0, "LOC_2B": 0, "LOC_1B": 0,
            "LOC_P": 0, "GB": 0, "FB": 1, "BUNT": 0,
        },
        "Wyatt Jones": {
            "BIP": 1, "LOC_LF": 1, "LOC_CF": 0, "LOC_RF": 0,
            "LOC_3B": 0, "LOC_SS": 0, "LOC_2B": 0, "LOC_1B": 0,
            "LOC_P": 0, "GB": 1, "FB": 0, "BUNT": 0,
        },
        "Rylan Kuklinski": {
            "BIP": 2, "LOC_LF": 0, "LOC_CF": 1, "LOC_RF": 0,
            "LOC_3B": 0, "LOC_SS": 1, "LOC_2B": 0, "LOC_1B": 0,
            "LOC_P": 0, "GB": 1, "FB": 1, "BUNT": 0,
        },
        "Charles Copus": {
            "BIP": 1, "LOC_LF": 0, "LOC_CF": 0, "LOC_RF": 0,
            "LOC_3B": 0, "LOC_SS": 1, "LOC_2B": 0, "LOC_1B": 0,
            "LOC_P": 0, "GB": 0, "FB": 1, "BUNT": 0,
        },
        "Kellen Smith": {
            "BIP": 0, "LOC_LF": 0, "LOC_CF": 0, "LOC_RF": 0,
            "LOC_3B": 0, "LOC_SS": 0, "LOC_2B": 0, "LOC_1B": 0,
            "LOC_P": 0, "GB": 0, "FB": 0, "BUNT": 0,
        },
    }

    for player, expected_stats in expected.items():
        for key, expected_value in expected_stats.items():
            assert stats[player][key] == expected_value