from cleaners.mlb_timeline_cleaner import clean_mlb_timeline_text
from models.timeline_block import TimelineBlockType


def test_mlb_timeline_marks_wild_pitch_as_game_event():

    raw = """
Major League Baseball

Wilyer Abreu walks.
Wild pitch by pitcher Reid Detmers. Wilyer Abreu to 2nd.
Willson Contreras flies out to left fielder Josh Lowe. 3 Outs
"""

    blocks = clean_mlb_timeline_text(raw)

    assert len(blocks) == 3
    assert blocks[0].block_type == TimelineBlockType.PLATE_APPEARANCE
    assert blocks[1].block_type == TimelineBlockType.GAME_EVENT
    assert blocks[1].event_type == "wild_pitch"
    assert blocks[2].block_type == TimelineBlockType.PLATE_APPEARANCE
