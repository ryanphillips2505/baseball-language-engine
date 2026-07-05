from models.game_event import GameEvent


def test_game_event_preserves_existing_fields():

    event = GameEvent(
        event_type="stolen_base",
        raw_text="Ceddanne Rafaela steals (11) 2nd base.",
        runner_name="Ceddanne Rafaela",
        base="2nd",
        source="mlb",
    )

    assert event.event_type == "stolen_base"
    assert event.raw_text == "Ceddanne Rafaela steals (11) 2nd base."
    assert event.runner_name == "Ceddanne Rafaela"
    assert event.base == "2nd"
    assert event.source == "mlb"


def test_game_event_supports_richer_baseball_context():

    event = GameEvent(
        event_type="pickoff",
        raw_text="Nolan Schanuel picked off 1st base.",
        runner_name="Nolan Schanuel",
        base="1st",
        from_base="1st",
        to_base=None,
        outcome="out",
        actor_name="Nolan Schanuel",
        credited_to="pitcher",
        source="mlb",
        metadata={
            "source_event": "runner_only",
        },
    )

    assert event.from_base == "1st"
    assert event.to_base is None
    assert event.outcome == "out"
    assert event.actor_name == "Nolan Schanuel"
    assert event.credited_to == "pitcher"
    assert event.metadata["source_event"] == "runner_only"
