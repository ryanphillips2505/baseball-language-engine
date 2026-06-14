from extractors.player_extractor import extract_batter_name


def test_extract_college_batter_name():
    assert extract_batter_name("J. Walk singled to center.") == "J. Walk"
    assert extract_batter_name("D. Lachance homered to left, C. Johnson scored.") == "D. Lachance"
    assert extract_batter_name("B. Brock walked.") == "B. Brock"
    assert extract_batter_name("J. Walk struck out looking.") == "J. Walk"