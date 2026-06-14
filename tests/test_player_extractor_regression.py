from extractors.player_extractor import extract_batter_name


def test_extract_college_batter_names():
    assert extract_batter_name("J. Walk singled to center.") == "J. Walk"
    assert extract_batter_name("D. Lachance homered to left, C. Johnson scored.") == "D. Lachance"
    assert extract_batter_name("B. Brock walked.") == "B. Brock"
    assert extract_batter_name("J. Walk struck out looking.") == "J. Walk"


def test_extract_mlb_batter_names():
    assert extract_batter_name("Nick Gonzales singles on a ground ball to center fielder Jakob Marsee.") == "Nick Gonzales"
    assert extract_batter_name("Bryan Reynolds grounds out, second baseman Xavier Edwards to first baseman Kyle Stowers.") == "Bryan Reynolds"


def test_extract_unknown_returns_none():
    assert extract_batter_name("") is None