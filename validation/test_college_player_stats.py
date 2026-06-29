from pathlib import Path

from aggregators.game_stat_aggregator import aggregate_game_stats
from pipeline.process_game import process_game


SAMPLE_PATH = Path("samples/college/raw/college_raw_game_01.txt")


def _stats():
    raw_text = SAMPLE_PATH.read_text(encoding="utf-8")
    game = process_game(raw_text)
    return aggregate_game_stats(game)


def test_college_stats_j_walk():
    stats = _stats()

    player = stats["J. Walk"]

    assert player["GP"] == 1
    assert player["K"] == 1
    assert player["BB"] == 2
    assert player["SB"] == 1
    assert player["BIP"] == 2
    assert player["LOC_LF"] == 1
    assert player["LOC_CF"] == 1
    assert player["FB"] == 1


def test_college_stats_d_lachance():
    stats = _stats()

    player = stats["D. Lachance"]

    assert player["GP"] == 1
    assert player["HR"] == 1
    assert player["XBH"] == 1
    assert player["BIP"] == 5
    assert player["LOC_LF"] == 1
    assert player["LOC_CF"] == 1
    assert player["LOC_3B"] == 1
    assert player["LOC_SS"] == 1
    assert player["LOC_2B"] == 1
    assert player["GB"] == 3
    assert player["XBH_LF"] == 1


def test_college_stats_b_brock():
    stats = _stats()

    player = stats["B. Brock"]

    assert player["GP"] == 1
    assert player["BB"] == 1
    assert player["2B"] == 1
    assert player["XBH"] == 1
    assert player["CS"] == 1
    assert player["BIP"] == 3
    assert player["LOC_LF"] == 1
    assert player["LOC_RF"] == 1
    assert player["LOC_SS"] == 1
    assert player["GB"] == 1
    assert player["FB"] == 1
    assert player["XBH_LF"] == 1