from adapters.opponent_iq_adapter import adapt_player_stats_to_opponent_iq


def test_opponent_iq_adapter_keeps_hits_and_locations_separate():
    player_stats = {
        "2B": 1,
        "3B": 1,
        "HR": 0,
        "XBH": 2,
        "LOC_2B": 3,
        "LOC_3B": 2,
        "GB-LOC_2B": 1,
        "FB-LOC_3B": 1,
        "LOC_CF": 4,
        "FB-LOC_CF": 2,
    }

    adapted = adapt_player_stats_to_opponent_iq(player_stats)

    assert adapted["2B"] == 1
    assert adapted["3B"] == 1
    assert adapted["XBH"] == 2

    assert "LOC_2B" not in adapted
    assert "LOC_3B" not in adapted

    assert adapted["CF"] == 4
    assert adapted["FB-CF"] == 2