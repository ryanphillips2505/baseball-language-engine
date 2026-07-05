from assemblers.game_event_builder import build_game_event
from models.timeline_block import GameEventBlock


def test_build_game_event_extracts_runner_and_base_from_stolen_base():

    event = build_game_event(
        GameEventBlock(
            raw_text="Ceddanne Rafaela steals (11) 2nd base.",
            event_type="stolen_base",
            source="mlb",
        )
    )

    assert event.runner_name == "Ceddanne Rafaela"
    assert event.base == "2nd"


def test_build_game_event_extracts_runner_and_base_from_caught_stealing():

    event = build_game_event(
        GameEventBlock(
            raw_text="Ceddanne Rafaela caught stealing 3rd base.",
            event_type="caught_stealing",
            source="mlb",
        )
    )

    assert event.runner_name == "Ceddanne Rafaela"
    assert event.base == "3rd"


def test_build_game_event_extracts_runner_from_pickoff():

    event = build_game_event(
        GameEventBlock(
            raw_text="Nolan Schanuel picked off 1st base, pitcher Jake Bennett to first baseman Willson Contreras.",
            event_type="pickoff",
            source="mlb",
        )
    )

    assert event.runner_name == "Nolan Schanuel"
    assert event.base == "1st"
