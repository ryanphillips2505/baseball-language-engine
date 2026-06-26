from pathlib import Path

from aggregators.game_stat_aggregator import aggregate_game_stats
from assemblers.plate_appearance_builder import build_plate_appearance
from cleaners.gamechanger_cleaner import clean_gamechanger_text
from models.game import Game


def test_full_game_parity():
    raw_text = Path("samples/gamechanger/raw/gamechanger_pa_blocks.txt").read_text()

    cleaned_blocks = clean_gamechanger_text(raw_text)

    game = Game(
        plate_appearances=[
            build_plate_appearance(block)
            for block in cleaned_blocks
        ]
    )

    stats = aggregate_game_stats(game)

    assert len(cleaned_blocks) == 163
    assert len(game.plate_appearances) == 163
    assert len(stats) > 0
