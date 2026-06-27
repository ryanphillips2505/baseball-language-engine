from aggregators.game_stat_aggregator import aggregate_game_stats
from assemblers.plate_appearance_builder import build_plate_appearance
from cleaners.gamechanger_cleaner import clean_gamechanger_text
from dataset.sample_paths import sample_path
from models.game import Game


def test_yukon_norman_known_player_stat_parity():
    raw_text = sample_path(
        "gamechanger",
        "gamechanger_pa_blocks.txt",
    ).read_text()

    cleaned_blocks = clean_gamechanger_text(raw_text)

    game = Game(
        plate_appearances=[
            build_plate_appearance(block)
            for block in cleaned_blocks
        ]
    )

    stats = aggregate_game_stats(game)

    assert len(cleaned_blocks) == 163

    assert stats["Drake Pace"]["2B"] == 1
    assert stats["Drake Pace"]["XBH"] == 1
    assert stats["Drake Pace"]["K"] == 1

    assert stats["Gentry Hoke"]["K"] == 1

    assert stats["Preston Klose"]["K"] == 1
    assert stats["Preston Klose"]["BB"] == 2
    assert stats["Preston Klose"]["3B"] == 1
    assert stats["Preston Klose"]["XBH"] == 1

    assert stats["Zayden Khalil"]["BB"] == 1
    assert stats["Zayden Khalil"]["HBP"] == 1

    assert stats["Brody Hailey"]["K"] == 1
    assert stats["Brody Hailey"]["HR"] == 1
    assert stats["Brody Hailey"]["XBH"] == 1