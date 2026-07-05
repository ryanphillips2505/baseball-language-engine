from assemblers.game_event_builder import build_game_event
from models.timeline_block import GameEventBlock


def test_stolen_base_context():

    event = build_game_event(
        GameEventBlock(
            raw_text="Ceddanne Rafaela steals (11) 2nd base.",
            event_type="stolen_base",
            source="mlb",
        )
    )

    assert event.actor_name == "Ceddanne Rafaela"
    assert event.runner_name == "Ceddanne Rafaela"
    assert event.from_base == "1st"
    assert event.to_base == "2nd"
    assert event.outcome == "safe"


def test_caught_stealing_context():

    event = build_game_event(
        GameEventBlock(
            raw_text="Ceddanne Rafaela caught stealing 3rd base.",
            event_type="caught_stealing",
            source="mlb",
        )
    )

    assert event.actor_name == "Ceddanne Rafaela"
    assert event.runner_name == "Ceddanne Rafaela"
    assert event.from_base == "2nd"
    assert event.to_base == "3rd"
    assert event.outcome == "out"


def test_pickoff_context():

    event = build_game_event(
        GameEventBlock(
            raw_text="Nolan Schanuel picked off 1st base.",
            event_type="pickoff",
            source="mlb",
        )
    )

    assert event.actor_name == "Nolan Schanuel"
    assert event.runner_name == "Nolan Schanuel"
    assert event.from_base == "1st"
    assert event.outcome == "out"


def test_wild_pitch_context():

    event = build_game_event(
        GameEventBlock(
            raw_text="Wild pitch by pitcher Jake Bennett. Josh Lowe to 2nd.",
            event_type="wild_pitch",
            source="mlb",
        )
    )

    assert event.runner_name == "Josh Lowe"
    assert event.to_base == "2nd"
    assert event.outcome == "advance"


def test_passed_ball_context():

    event = build_game_event(
        GameEventBlock(
            raw_text="Passed ball by catcher Carlos Narváez. Josh Lowe to 2nd.",
            event_type="passed_ball",
            source="mlb",
        )
    )

    assert event.runner_name == "Josh Lowe"
    assert event.to_base == "2nd"
    assert event.outcome == "advance"
