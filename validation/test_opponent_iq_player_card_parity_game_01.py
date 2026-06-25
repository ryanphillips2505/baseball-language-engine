from pathlib import Path

from aggregators.game_stat_aggregator import aggregate_game_stats
from aggregators.swing_decision_aggregator import aggregate_swing_decisions
from assemblers.gamechanger_swing_game_builder import build_gamechanger_swing_game
from assemblers.plate_appearance_builder import build_plate_appearance
from cleaners.gamechanger_cleaner import clean_gamechanger_text
from models.game import Game
from translators.player_card_translator import build_player_card


SAMPLE_PATH = Path(
    "samples/gamechanger/risin_shockers_2026_06_04.txt"
)


def build_stat_game(raw_text: str) -> Game:
    cleaned = clean_gamechanger_text(raw_text)

    return Game(
        plate_appearances=[
            build_plate_appearance(block)
            for block in cleaned
        ]
    )


def test_opponent_iq_player_card_parity_game_01():
    raw_text = SAMPLE_PATH.read_text(encoding="utf-8")

    stat_game = build_stat_game(raw_text)
    game_stats = aggregate_game_stats(stat_game)

    swing_game = build_gamechanger_swing_game(raw_text)
    swing_stats = aggregate_swing_decisions(swing_game)

    card = build_player_card(
        "Wade Webb",
        game_stats=game_stats,
        swing_stats=swing_stats,
    )

    assert card["Player"] == "Wade Webb"

    assert card["Season Summary"]["GP"] == 1
    assert card["Season Summary"]["2B"] == 1
    assert card["Season Summary"]["3B"] == 1
    assert card["Season Summary"]["XBH"] == 2
    assert card["Season Summary"]["BIP"] == 3

    assert card["Spray Zone"]["LOC_LF"] == 1
    assert card["Spray Zone"]["LOC_CF"] == 2
    assert card["Spray Zone"]["FB"] == 3

    assert card["Damage"]["XBH"] == 2
    assert card["Damage"]["XBH_CF"] == 2

    assert card["Swing Decision"]["0-0"]["PA"] == 3
    assert card["Swing Decision"]["3-2"]["BIP"] == 1