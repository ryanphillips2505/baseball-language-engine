from pathlib import Path

from aggregators.game_stat_aggregator import aggregate_game_stats
from assemblers.plate_appearance_builder import build_plate_appearance
from cleaners.gamechanger_cleaner import clean_gamechanger_text
from models.game import Game


def test_yukon_norman_boxscore_parity():
    raw_text = Path("samples/yukon_norman_2026_03_02_raw.txt").read_text()

    cleaned_blocks = clean_gamechanger_text(raw_text)
    
    assert len(cleaned_blocks) == 50

    game = Game(
        plate_appearances=[
            build_plate_appearance(block)
            for block in cleaned_blocks
        ]
    )

    stats = aggregate_game_stats(game)

    assert stats["Zayden Khalil"]["BB"] == 2
    assert stats["Zayden Khalil"]["SB"] == 1

    assert stats["Eddie Fish"]["BB"] == 1
    assert stats["Eddie Fish"]["K"] == 2

    assert stats["Drake Pace"]["2B"] == 1
    assert stats["Drake Pace"]["XBH"] == 1

    assert stats["Wyatt Jones"]["K"] == 1
    assert stats["Wyatt Jones"]["CS"] == 1

    assert stats["Gentry Hoke"]["K"] == 2

    assert stats["Preston Klose"]["K"] == 1
    assert stats["Preston Klose"]["CS"] == 1

    assert stats["Owen Blair"]["K"] == 1

    assert stats["Caleb Schneider"]["BB"] == 1
    assert stats["Caleb Schneider"]["K"] == 1