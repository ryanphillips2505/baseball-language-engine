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


def test_opponent_iq_season_parity_game_01():
    raw_text = SAMPLE_PATH.read_text(encoding="utf-8")
    game = build_game(raw_text)
    stats = aggregate_game_stats(game)

    expected = {
        "Wade Webb": {
            "GP": 1, "K": 0, "BB": 0, "HBP": 0,
            "BIP": 3, "GB": 0, "FB": 3, "BUNT": 0,
            "SB": 0, "CS": 0,
        },
        "Miles Stanley": {
            "GP": 1, "K": 0, "BB": 2, "HBP": 0,
            "BIP": 1, "GB": 0, "FB": 1, "BUNT": 0,
            "SB": 0, "CS": 0,
        },
        "Traylon Barnes": {
            "GP": 1, "K": 0, "BB": 2, "HBP": 0,
            "BIP": 1, "GB": 0, "FB": 1, "BUNT": 0,
            "SB": 0, "CS": 0,
        },
        "Wyatt Jones": {
            "GP": 1, "K": 0, "BB": 1, "HBP": 1,
            "BIP": 1, "GB": 1, "FB": 0, "BUNT": 0,
            "SB": 0, "CS": 0,
        },
        "Rylan Kuklinski": {
            "GP": 1, "K": 0, "BB": 0, "HBP": 1,
            "BIP": 2, "GB": 1, "FB": 1, "BUNT": 0,
            "SB": 0, "CS": 0,
        },
        "Charles Copus": {
            "GP": 1, "K": 1, "BB": 1, "HBP": 0,
            "BIP": 1, "GB": 0, "FB": 1, "BUNT": 0,
            "SB": 0, "CS": 0,
        },
        "Kellen Smith": {
            "GP": 1, "K": 1, "BB": 1, "HBP": 1,
            "BIP": 0, "GB": 0, "FB": 0, "BUNT": 0,
            "SB": 0, "CS": 1,
        },
    }

    for player, expected_stats in expected.items():
        for key, expected_value in expected_stats.items():
            assert stats[player][key] == expected_value, (
                f"{player} {key}: expected {expected_value}, "
                f"got {stats[player][key]}"
            )