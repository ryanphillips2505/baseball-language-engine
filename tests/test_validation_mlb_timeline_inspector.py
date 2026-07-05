from tools.inspection.ble_inspector import inspect_ble_file


def test_mlb_inspector_uses_timeline_events_without_counting_them_as_plate_appearances():

    data = inspect_ble_file(
        "samples/mlb/validation/red_sox_angels_2026_07_04.txt"
    )

    assert data["source"] == "mlb"
    assert data["timeline_count"] == 75
    assert data["plate_appearance_count"] == 72

    events = data["timeline_game_events"]

    assert [event["event_type"] for event in events] == [
        "stolen_base",
        "wild_pitch",
        "wild_pitch",
    ]
