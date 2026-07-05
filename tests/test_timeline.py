from models.timeline import Timeline
from models.timeline_block import GameEventBlock, PlateAppearanceBlock


def test_timeline_starts_empty():
    timeline = Timeline()

    assert len(timeline) == 0
    assert timeline.blocks == []


def test_timeline_appends_blocks_in_order():
    timeline = Timeline()

    pa = PlateAppearanceBlock("John Smith singles to center field.")
    event = GameEventBlock("Runner advances on a wild pitch.", event_type="wild_pitch")

    timeline.append(pa)
    timeline.append(event)

    assert list(timeline) == [pa, event]
    assert len(timeline) == 2


def test_timeline_filters_plate_appearance_and_game_event_blocks():
    timeline = Timeline()

    pa = PlateAppearanceBlock("John Smith singles to center field.")
    event = GameEventBlock("Runner advances on a wild pitch.", event_type="wild_pitch")

    timeline.extend([pa, event])

    assert timeline.plate_appearance_blocks() == [pa]
    assert timeline.game_event_blocks() == [event]
