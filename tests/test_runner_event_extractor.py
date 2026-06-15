from extractors.runner_event_extractor import extract_runner_events


def test_extract_sb_second():
    events = extract_runner_events(
        "John Smith steals second base."
    )

    assert len(events) == 1
    assert events[0].event_type == "SB"
    assert events[0].base == "2B"


def test_extract_sb_third():
    events = extract_runner_events(
        "John Smith steals third base."
    )

    assert len(events) == 1
    assert events[0].event_type == "SB"
    assert events[0].base == "3B"


def test_extract_cs_second():
    events = extract_runner_events(
        "John Smith caught stealing second base."
    )

    assert len(events) == 1
    assert events[0].event_type == "CS"
    assert events[0].base == "2B"


def test_extract_cs_third():
    events = extract_runner_events(
        "John Smith caught stealing third base."
    )

    assert len(events) == 1
    assert events[0].event_type == "CS"
    assert events[0].base == "3B"


def test_extract_mlb_style():
    events = extract_runner_events(
        "Runner steals 2nd."
    )

    assert len(events) == 1
    assert events[0].event_type == "SB"
    assert events[0].base == "2B"


def test_extract_college_style():
    events = extract_runner_events(
        "stole third"
    )

    assert len(events) == 1
    assert events[0].event_type == "SB"
    assert events[0].base == "3B"


def test_no_runner_event():
    events = extract_runner_events(
        "struck out swinging"
    )

    assert events == []