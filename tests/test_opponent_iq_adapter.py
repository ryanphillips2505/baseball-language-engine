from adapters.opponent_iq_adapter import adapt_player_stats_to_opponent_iq


def test_opponent_iq_adapter_keeps_hits_and_locations_separate():
    player_stats = {
        "2B": 1,
        "3B": 0,
        "HR": 0,
        "XBH": 1,
        "LOC_2B": 3,
        "LOC_3B": 2,
        "GB-LOC_2B": 1,
        "FB-LOC_3B": 1,
    }

    adapted = adapt_player_stats_to_opponent_iq(player_stats)

    assert adapted["hitting"]["2B"] == 1
    assert adapted["hitting"]["XBH"] == 1

    assert adapted["locations"]["2B"] == 3
    assert adapted["locations"]["3B"] == 2

    assert adapted["combos"]["GB-2B"] == 1
    assert adapted["combos"]["FB-3B"] == 1