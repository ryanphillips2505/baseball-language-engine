from classifiers.location_classifier import classify_location


def test_outfield_locations():
    assert classify_location("J. Walk singled to center.") == "CF"
    assert classify_location("B. Brock flied out to right.") == "RF"
    assert classify_location("D. Lachance homered to left.") == "LF"


def test_infield_locations():
    assert classify_location("grounded out to shortstop.") == "SS"
    assert classify_location("grounded out to second.") == "2B"
    assert classify_location("grounded out to third.") == "3B"
    assert classify_location("grounded out to first.") == "1B"
    assert classify_location("grounded out to pitcher.") == "P"


def test_unknown_location():
    assert classify_location("walked.") is None
