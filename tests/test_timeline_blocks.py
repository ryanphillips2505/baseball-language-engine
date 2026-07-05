from models.timeline_block import (
    GameEventBlock,
    PlateAppearanceBlock,
    TimelineBlockType,
)


def test_plate_appearance_block_is_timeline_block():
    block = PlateAppearanceBlock(
        raw_text="John Smith singles on a line drive to center field.",
        source="mlb",
        inning="Top 1st",
    )

    assert block.block_type == TimelineBlockType.PLATE_APPEARANCE
    assert block.raw_text == "John Smith singles on a line drive to center field."
    assert block.source == "mlb"
    assert block.inning == "Top 1st"
    assert block.metadata == {}


def test_game_event_block_can_represent_runner_only_event():
    block = GameEventBlock(
        raw_text="Ceddanne Rafaela steals (11) 2nd base.",
        event_type="stolen_base",
        source="mlb",
    )

    assert block.block_type == TimelineBlockType.GAME_EVENT
    assert block.event_type == "stolen_base"
    assert block.raw_text == "Ceddanne Rafaela steals (11) 2nd base."
    assert block.source == "mlb"


def test_timeline_blocks_do_not_require_batter_or_plate_appearance():
    block = GameEventBlock(
        raw_text="Runner advances on a wild pitch.",
        event_type="wild_pitch",
    )

    assert not hasattr(block, "batter")
    assert block.event_type == "wild_pitch"
