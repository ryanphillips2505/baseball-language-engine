from extractors.pitch_token_extractor import extract_pitch_tokens


def test_extracts_pitch_tokens_from_single_line():
    block = [
        "Ball 1, Strike 1 looking, Foul, In play.",
    ]

    assert extract_pitch_tokens(block) == [
        "Ball 1",
        "Strike 1 looking",
        "Foul",
        "In play",
    ]


def test_extracts_pitch_tokens_across_multiple_lines():
    block = [
        "Ball 1",
        "Strike 1 swinging",
        "Foul tip",
        "In play.",
    ]

    assert extract_pitch_tokens(block) == [
        "Ball 1",
        "Strike 1 swinging",
        "Foul tip",
        "In play",
    ]


def test_ignores_non_pitch_text():
    block = [
        "John Smith doubles on a fly ball to right field.",
        "Runner scores.",
    ]

    assert extract_pitch_tokens(block) == []


def test_extracts_bunt_foul_variants():
    block = [
        "Foul bunt, Bunt foul",
    ]

    assert extract_pitch_tokens(block) == [
        "Foul bunt",
        "Bunt foul",
    ]