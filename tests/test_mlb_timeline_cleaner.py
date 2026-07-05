from cleaners.mlb_timeline_cleaner import clean_mlb_timeline_text
from models.timeline_block import TimelineBlockType


def test_mlb_timeline_cleaner_marks_caught_stealing_as_game_event():

    raw = """
Major League Baseball

Anthony Seigler walks.
Ceddanne Rafaela caught stealing 2nd base, catcher Logan O'Hoppe to second baseman Luis Rengifo.
Wilyer Abreu walks.
"""

    blocks = clean_mlb_timeline_text(raw)

    assert len(blocks) == 3

    assert blocks[0].block_type == TimelineBlockType.PLATE_APPEARANCE

    assert blocks[1].block_type == TimelineBlockType.GAME_EVENT
    assert blocks[1].event_type == "caught_stealing"
    assert "caught stealing" in blocks[1].raw_text

    assert blocks[2].block_type == TimelineBlockType.PLATE_APPEARANCE


def test_existing_mlb_cleaner_still_returns_strings():

    from cleaners.mlb_cleaner import clean_mlb_text

    raw = """
Major League Baseball

Anthony Seigler walks.
Ceddanne Rafaela caught stealing 2nd base, catcher Logan O'Hoppe to second baseman Luis Rengifo.
"""

    cleaned = clean_mlb_text(raw)

    assert cleaned == [
        "Anthony Seigler walks.",
        "Ceddanne Rafaela caught stealing 2nd base, catcher Logan O'Hoppe to second baseman Luis Rengifo.",
    ]
