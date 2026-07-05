from models.game_event import GameEvent


def test_game_event_model_stores_non_pa_event():
    event = GameEvent(
        event_type="stolen_base",
        raw_text="Ceddanne Rafaela steals (11) 2nd base.",
        runner_name="Ceddanne Rafaela",
        base="2B",
        source="mlb",
    )

    assert event.event_type == "stolen_base"
    assert event.runner_name == "Ceddanne Rafaela"
    assert event.base == "2B"
    assert event.source == "mlb"
