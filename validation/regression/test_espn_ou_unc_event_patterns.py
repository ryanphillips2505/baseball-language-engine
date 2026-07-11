from extractors.player_extractor import extract_batter_name
from extractors.runner_event_extractor import extract_runner_events


def test_espn_past_tense_sacrifice_fly_preserves_batter():
    text = (
        "C. Hynek hit sacrifice fly to right, "
        "G. Gallaher scored, E. Paulsen to third."
    )

    assert extract_batter_name(text) == "C. Hynek"


def test_espn_past_tense_sacrifice_bunts_preserve_batters():
    cases = {
        (
            "K. Branch hit sacrifice bunt to pitcher, "
            "D. Tockey to third."
        ): "K. Branch",
        (
            "D. Tockey hit sacrifice bunt to first, "
            "D. Harris to second."
        ): "D. Tockey",
    }

    for text, expected_batter in cases.items():
        assert extract_batter_name(text) == expected_batter


def test_espn_picked_off_and_caught_stealing_extracts_one_runner_event():
    text = (
        "J. Willits picked off and caught stealing second, "
        "pitcher to first to second."
    )

    events = extract_runner_events(text)

    assert len(events) == 1

    event = events[0]

    assert event.event_type == "CS"
    assert event.base == "2B"
    assert event.runner_name == "J. Willits"


def test_standard_caught_stealing_wording_remains_supported():
    events = extract_runner_events(
        "Miles Stanley caught stealing second."
    )

    assert len(events) == 1

    event = events[0]

    assert event.event_type == "CS"
    assert event.base == "2B"
    assert event.runner_name == "Miles Stanley"
