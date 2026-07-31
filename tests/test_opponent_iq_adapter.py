from adapters.opponent_iq_adapter import adapt_player_stats_to_opponent_iq


def test_opponent_iq_adapter_matches_legacy_1b_2b_3b_location_collision():
    player_stats = {
        "1B": 2,
        "2B": 1,
        "3B": 1,
        "HR": 0,
        "XBH": 2,
        "LOC_1B": 4,
        "LOC_2B": 3,
        "LOC_3B": 2,
        "GB-LOC_1B": 2,
        "GB-LOC_2B": 1,
        "FB-LOC_3B": 1,
        "LOC_CF": 4,
        "FB-LOC_CF": 2,
    }

    adapted = adapt_player_stats_to_opponent_iq(player_stats)

    assert adapted["1B"] == 6
    assert adapted["2B"] == 4
    assert adapted["3B"] == 3
    assert adapted["HR"] == 0
    assert adapted["XBH"] == 2

    assert adapted["CF"] == 4

    assert adapted["GB-1B"] == 2
    assert adapted["GB-2B"] == 1
    assert adapted["FB-3B"] == 1
    assert adapted["FB-CF"] == 2