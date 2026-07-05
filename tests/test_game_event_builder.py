from assemblers.game_event_builder import build_game_event
from models.timeline_block import GameEventBlock


def test_build_game_event_from_caught_stealing_block():

    event = build_game_event(
        GameEventBlock(
            raw_text="Ceddanne Rafaela caught stealing 2nd base.",
            event_type="caught_stealing",
            source="mlb",
        )
    )

    assert event.event_type == "caught_stealing"
    assert event.base == "2nd"
    assert event.source == "mlb"


def test_build_game_event_from_stolen_base_block():

    event = build_game_event(
        GameEventBlock(
            raw_text="Ceddanne Rafaela steals (11) 2nd base.",
            event_type="stolen_base",
            source="mlb",
        )
    )

    assert event.event_type == "stolen_base"
    assert event.base == "2nd"
    assert event.source == "mlb"
