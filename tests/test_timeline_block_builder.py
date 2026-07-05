from assemblers.timeline_block_builder import build_timeline_blocks
from models.timeline_block import TimelineBlockType


def test_string_input_produces_timeline_block():

    blocks = build_timeline_blocks([
        "John Smith singles to center."
    ])

    assert len(blocks) == 1
    assert blocks[0].block_type == TimelineBlockType.PLATE_APPEARANCE


def test_multiple_strings_produce_multiple_blocks():

    blocks = build_timeline_blocks([
        "One",
        "Two",
        "Three",
    ])

    assert len(blocks) == 3
