from assemblers.timeline_event_builder import append_game_event
from models.timeline import Timeline
from models.timeline_block import GameEventBlock


def test_append_game_event():

    timeline = Timeline()

    append_game_event(
        timeline,
        GameEventBlock(
            raw_text="Runner steals second.",
            event_type="stolen_base",
        ),
    )

    assert len(timeline) == 1
    assert timeline.game_event_blocks()[0].event_type == "stolen_base"
