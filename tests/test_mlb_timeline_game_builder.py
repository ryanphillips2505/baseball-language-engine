from assemblers.game_builder import build_game
from cleaners.mlb_timeline_cleaner import clean_mlb_timeline_text
from models.game_event import GameEvent
from models.timeline_block import GameEventBlock, TimelineBlockType


def test_build_game_from_mlb_timeline_blocks_excludes_game_events_from_plate_appearances():

    raw = """
Major League Baseball

Anthony Seigler walks.
Ceddanne Rafaela caught stealing 2nd base, catcher Logan O'Hoppe to second baseman Luis Rengifo.
Wilyer Abreu walks.
"""

    timeline_blocks = clean_mlb_timeline_text(raw)
    game = build_game(timeline_blocks)

    assert len(game.plate_appearances) == 2
    assert len(game.timeline) == 3

    assert game.timeline.blocks[0].block_type == TimelineBlockType.PLATE_APPEARANCE
    assert game.timeline.blocks[1].block_type == TimelineBlockType.GAME_EVENT
    assert game.timeline.blocks[2].block_type == TimelineBlockType.PLATE_APPEARANCE


def test_build_game_from_mlb_timeline_blocks_attaches_game_event_model():

    raw = """
Major League Baseball

Anthony Seigler walks.
Ceddanne Rafaela steals (11) 2nd base.
Wilyer Abreu walks.
"""

    timeline_blocks = clean_mlb_timeline_text(raw)
    game = build_game(timeline_blocks)

    event_block = game.timeline.blocks[1]

    assert isinstance(event_block, GameEventBlock)
    assert event_block.event_type == "stolen_base"
    assert isinstance(event_block.metadata["game_event"], GameEvent)
    assert event_block.metadata["game_event"].event_type == "stolen_base"
    assert event_block.metadata["game_event"].base == "2nd"
    assert event_block.metadata["game_event"].source == "mlb"
