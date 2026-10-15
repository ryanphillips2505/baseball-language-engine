"""SIDEARM wordings and StatCrew ball types used by college SCOUTBINDERs."""

import pytest

from aggregators.game_stat_aggregator import aggregate_game_stats
from language.names import RosterMatcher
from pipeline.process_game import process_game

FILLER = "\n".join(
    [
        "Bottom of 1st",
        "A, B. struck out looking.",
        "C, D. struck out looking.",
        "E, F. struck out looking.",
        "G, H. struck out looking.",
        "I, J. struck out looking.",
    ]
)


def _player(line: str, name: str) -> dict:
    stats = aggregate_game_stats(process_game(f"Top of 1st\n{line}\n{FILLER}\n"))
    return stats[name]


@pytest.mark.parametrize(
    ("line", "name", "ball_type", "location"),
    [
        ("Ruben Castro sacrifice fly to rf, RBI (1-2 KKB); Hank Heiselbetz scored. 3 1", "Ruben Castro", "FB", "LOC_RF"),
        ("Ruben Castro flew into double play to rf (2-2 BSBS); Hank Heiselbetz out at 1B on the play. 3 1", "Ruben Castro", "FB", "LOC_RF"),
        ("Ruben Castro flew out to rf (1-2 KKB). 3 1", "Ruben Castro", "FB", "LOC_RF"),
        ("Austin Wallace sacrifice bunt to first base, unassisted, RBI (0-0). 3 1", "Austin Wallace", "BUNT", "LOC_1B"),
        ("Colton Kinnie reached first on a throwing error by ss.", "Colton Kinnie", "GB", "LOC_SS"),
    ],
)
def test_sidearm_bare_wordings_are_balls_in_play(line, name, ball_type, location):
    player = _player(line, name)

    assert player["BIP"] == 1
    assert player[ball_type] == 1
    assert player[location] == 1


@pytest.mark.parametrize(
    ("line", "ball_type"),
    [
        ("Smith, J. singled to left field.", "GB"),     # single to the outfield
        ("Smith, J. doubled to left field.", "FB"),     # extra bases to the outfield
        ("Smith, J. out at first 1b to p.", "GB"),      # infield, no ball type stated
        ("Smith, J. lined out to cf.", "FB"),           # stated ball type wins
    ],
)
def test_statcrew_ball_type_follows_the_presto_lane_rule(line, ball_type):
    player = _player(line, "Smith, J.")

    assert player[ball_type] == 1
    assert player["GB"] + player["FB"] + player["BUNT"] == 1


def test_ball_type_inference_is_college_only():
    # MLB wording without a stated ball type stays unclassified.
    from language.reader import build_multi_platform_plate_appearance

    pa = build_multi_platform_plate_appearance("Aaron Judge singles to left fielder Riley Greene.")
    assert pa.ball_type is None


def test_glued_suffix_names_match_the_roster():
    matcher = RosterMatcher(["Guerrero Jr., Adrian", "Chris Benavidez"])

    assert matcher.match("Adrian GuerreroJr") == "Guerrero Jr., Adrian"
    assert matcher.match("GuerreroJr,Adrian") == "Guerrero Jr., Adrian"


def test_dropped_third_strike_reach_is_still_a_strikeout():
    player = _player("R. Requejo struck out, reached first on an error by c.", "R. Requejo")

    assert player["K"] == 1
    assert player["BIP"] == 0


@pytest.mark.parametrize(
    ("line", "ball_type", "location"),
    [
        ("Logan Jeske singled to left center.", "FB", "LOC_LF"),
        ("Mason Shimkus singled to shallow center field (0-0).", "FB", "LOC_CF"),
        ("Logan Jeske singled up the middle.", "GB", "LOC_CF"),
        ("Diego Sotelo grounded out, ss to 1b (1-0 B).", "GB", "LOC_SS"),
        ("Blake Seefeldt grounded into double play ss to 2b to 1b; Ryan Strickland out on the play.", "GB", "LOC_SS"),
    ],
)
def test_statcrew_spray_matches_the_fielder_who_played_the_ball(line, ball_type, location):
    name = " ".join(line.split()[:2])
    player = _player(line, name)

    assert player[ball_type] == 1
    assert player[location] == 1


def test_batter_advance_is_not_a_fielder_location():
    player = _player("Tyler Akers doubled, advanced to third on the throw, RBI.", "Tyler Akers")

    assert player["LOC_3B"] == 0
