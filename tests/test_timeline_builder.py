from assemblers.timeline_builder import build_timeline


def test_build_timeline_returns_timeline():

    timeline = build_timeline([
        "John Smith singles."
    ])

    assert len(timeline) == 1


def test_build_timeline_multiple():

    timeline = build_timeline([
        "One",
        "Two",
    ])

    assert len(timeline) == 2
