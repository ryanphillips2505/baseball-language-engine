from assemblers.game_builder import build_game
from models.timeline_block import TimelineBlockType


def test_builder_creates_matching_timeline():
    game = build_game([
        "John Smith singles to center field."
    ])

    assert len(game.plate_appearances) == 1
    assert len(game.timeline) == 1

    block = list(game.timeline)[0]

    assert block.block_type == TimelineBlockType.PLATE_APPEARANCE


def test_builder_keeps_plate_appearance_count_equal_to_timeline():
    game = build_game([
        "John Smith singles to center field.",
        "Mike Jones strikes out swinging."
    ])

    assert len(game.timeline) == len(game.plate_appearances)
