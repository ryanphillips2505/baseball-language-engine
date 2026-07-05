from cleaners.mlb_timeline_cleaner import clean_mlb_timeline_text
from models.timeline_block import TimelineBlockType


def test_mlb_timeline_marks_balk_as_game_event():

    raw = """
Major League Baseball

Nolan Schanuel walks.
Balk by pitcher Jake Bennett. Nolan Schanuel to 2nd.
Denzer Guzman strikes out.
"""

    blocks = clean_mlb_timeline_text(raw)

    assert len(blocks) == 3
    assert blocks[0].block_type == TimelineBlockType.PLATE_APPEARANCE
    assert blocks[1].block_type == TimelineBlockType.GAME_EVENT
    assert blocks[1].event_type == "balk"
    assert blocks[2].block_type == TimelineBlockType.PLATE_APPEARANCE
