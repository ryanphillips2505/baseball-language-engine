from adapters.opponent_iq_engine_adapter import process_raw_text_to_opponent_iq_game


def test_gc_bunts_out_count_as_bip_ground_ball_locations():
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
    assert players["John Crosby"]["GB"] == 1
    assert players["John Crosby"]["P"] == 1
    assert players["John Crosby"]["GB-P"] == 1

    assert players["Ben Rogalski"]["BIP"] == 1
    assert players["Ben Rogalski"]["GB"] == 1
    assert players["Ben Rogalski"]["3B"] == 1
    assert players["Ben Rogalski"]["GB-3B"] == 1
