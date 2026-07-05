from assemblers.timeline_game_event_extractor import extract_game_events
from models.timeline_block import (
    PlateAppearanceBlock,
    GameEventBlock,
)


def test_returns_only_game_events():

    blocks = [
        PlateAppearanceBlock(
            raw_text="Single"
        ),
        GameEventBlock(
            raw_text="Runner steals second.",
            event_type="stolen_base",
        ),
        PlateAppearanceBlock(
            raw_text="Strikeout"
        ),
        GameEventBlock(
            raw_text="Wild pitch.",
            event_type="wild_pitch",
        ),
    ]

    events = extract_game_events(blocks)

    assert len(events) == 2
    assert events[0].event_type == "stolen_base"
    assert events[1].event_type == "wild_pitch"
