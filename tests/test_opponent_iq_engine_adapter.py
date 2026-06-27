from adapters.opponent_iq_engine_adapter import process_raw_text_to_opponent_iq_stats


def test_process_raw_text_to_opponent_iq_stats():
    raw_text = """
    All Plays
    Top 1st
    John Smith singles on a line drive to center fielder.
    """

    stats = process_raw_text_to_opponent_iq_stats(raw_text)

    assert "John Smith" in stats
    assert stats["John Smith"]["BIP"] == 1
    assert stats["John Smith"]["CF"] == 1