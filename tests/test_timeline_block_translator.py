from translators.timeline_block_translator import translate_timeline_blocks
from models.timeline_block import TimelineBlockType


def test_translate_strings_to_timeline_blocks():

    blocks = translate_timeline_blocks([
        "John Smith singles.",
        "Mike Jones strikes out.",
    ])

    assert len(blocks) == 2
    assert all(
        b.block_type == TimelineBlockType.PLATE_APPEARANCE
        for b in blocks
    )
