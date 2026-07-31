from cleaners.mlb_cleaner import clean_mlb_text


def test_mlb_cleaner_keeps_strikeout_swinging_play_lines():
    raw_text = "\n".join(
        [
            "Vaughn Grissom strikes out swinging.",
            "Jonah Heim strikes out swinging.",
            "Jo Adell strikes out swinging. 3 Outs",
        ]
    )

    cleaned = clean_mlb_text(raw_text)

    assert "Vaughn Grissom strikes out swinging." in cleaned
    assert "Jonah Heim strikes out swinging." in cleaned
    assert "Jo Adell strikes out swinging. 3 Outs" in cleaned


def test_mlb_cleaner_rejects_pitcher_strikes_out_batter_captions():
    raw_text = "\n".join(
        [
            "Reid Detmers strikes out Nate Eaton",
            "Sonny Gray strikes out Brandon Nimmo",
            "Nate Eaton strikes out swinging. 1 Out",
        ]
    )

    cleaned = clean_mlb_text(raw_text)

    assert cleaned == ["Nate Eaton strikes out swinging. 1 Out"]


def test_mlb_cleaner_keeps_throwing_and_missed_catch_errors_via_statsapi_wording():
    from detectors.event_detector import detect_event_types
    from models.types import EventType

    throwing = (
        "Jose Siri reaches on a throwing error by third baseman Max Muncy. "
        "Donovan Walton to 2nd."
    )
    missed = (
        "Willson Contreras reaches on a missed catch error by first baseman "
        "Nolan Schanuel, assist to third baseman Denzer Guzman."
    )

    assert detect_event_types(throwing)[0].event_type == EventType.ERROR
    assert detect_event_types(missed)[0].event_type == EventType.ERROR
