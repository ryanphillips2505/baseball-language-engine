from cleaners.mlb_timeline_cleaner import clean_mlb_timeline_text
from models.timeline_block import TimelineBlockType


def test_mlb_timeline_marks_pickoff_as_game_event():

    raw = """
Major League Baseball

Nolan Schanuel singles on a line drive to center fielder Ceddanne Rafaela.
Nolan Schanuel picked off 1st base, pitcher Jake Bennett to first baseman Willson Contreras.
Denzer Guzman strikes out swinging.
"""

    blocks = clean_mlb_timeline_text(raw)

    assert len(blocks) == 3
    assert blocks[0].block_type == TimelineBlockType.PLATE_APPEARANCE
    assert blocks[1].block_type == TimelineBlockType.GAME_EVENT
    assert blocks[1].event_type == "pickoff"
    assert blocks[2].block_type == TimelineBlockType.PLATE_APPEARANCE
    assert "strikes out swinging" in blocks[2].raw_text


def test_mlb_timeline_marks_picked_off_and_caught_stealing_as_game_event():

    raw = """
Major League Baseball

Nolan Schanuel walks.
Nolan Schanuel picked off and caught stealing 2nd base, pitcher Jake Bennett to first baseman Willson Contreras to shortstop Andruw Monasterio.
Denzer Guzman strikes out swinging.
"""

    blocks = clean_mlb_timeline_text(raw)

    assert len(blocks) == 3
    assert blocks[1].block_type == TimelineBlockType.GAME_EVENT
    assert blocks[1].event_type == "caught_stealing"
    assert blocks[2].block_type == TimelineBlockType.PLATE_APPEARANCE
    assert "strikes out swinging" in blocks[2].raw_text
