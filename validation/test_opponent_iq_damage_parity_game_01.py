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


def test_opponent_iq_damage_parity_game_01():
    raw_text = SAMPLE_PATH.read_text(encoding="utf-8")
    game = build_game(raw_text)
    stats = aggregate_game_stats(game)

    expected = {
        "Wade Webb": {
            "XBH": 2,
            "XBH_LF": 0,
            "XBH_CF": 2,
            "XBH_RF": 0,
        },
        "Miles Stanley": {
            "XBH": 1,
            "XBH_LF": 1,
            "XBH_CF": 0,
            "XBH_RF": 0,
        },
        "Traylon Barnes": {
            "XBH": 1,
            "XBH_LF": 1,
            "XBH_CF": 0,
            "XBH_RF": 0,
        },
    }

    for player, expected_stats in expected.items():
        for key, expected_value in expected_stats.items():
            assert stats[player][key] == expected_value, (
                f"{player} {key}: expected {expected_value}, "
                f"got {stats[player][key]}"
            )