from adapters.opponent_iq_engine_adapter import process_raw_text_to_opponent_iq_game


def test_gc_bunts_out_count_as_legacy_bunt_locations():
    raw_text = """
    All Plays

    Bottom 6th - Bixby Varsity Spartans
    Ground Out
    2 Outs
    In play.
    John Crosby bunts out, pitcher to first baseman .

    Bottom 4th - Bixby Varsity Spartans
    Ground Out
    2 Outs
    In play.
    Ben Rogalski bunts out, third baseman to first baseman .
    """

    team, players = process_raw_text_to_opponent_iq_game(raw_text)

    assert players["John Crosby"]["BIP"] == 1
    assert players["John Crosby"]["BUNT"] == 1
    assert players["John Crosby"]["BUNT-P"] == 1
    assert players["John Crosby"]["GB"] == 0

    assert players["Ben Rogalski"]["BIP"] == 1
    assert players["Ben Rogalski"]["BUNT"] == 1
    assert players["Ben Rogalski"]["BUNT-3B"] == 1
    assert players["Ben Rogalski"]["GB"] == 0

    assert team["BIP"] == 2
    assert team["BUNT"] == 2
    assert team["BUNT-P"] == 1
    assert team["BUNT-3B"] == 1
