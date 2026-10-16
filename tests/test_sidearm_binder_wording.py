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


def test_statcrew_sac_without_the_word_bunt_is_a_bunt():
    player = _player("Max Tremblay grounded out to 3b, SAC; Bill McCarter advanced to second.", "Max Tremblay")

    assert player["BUNT"] == 1
    assert player["GB"] == 0
    assert player["LOC_3B"] == 1


@pytest.mark.parametrize(
    ("line", "expect"),
    [
        ("Isaac Webb homered, 3 RBI; Dagen Brewer scored.", {"BIP": 1, "HR": 1, "FB": 1}),
        ("Dagen Brewer doubled, ground-rule (0-1 F); Eric Bacon advanced to third.", {"BIP": 1, "FB": 1}),
        ("Seth Dandridge singled, advanced to second on an error by cf (1-2 KBF).", {"H": 1, "GB": 1, "LOC_CF": 1}),
        ("Landon Bruce singled, bunt, advanced to second on a throwing error by c (0-0).", {"H": 1, "BUNT": 1, "LOC_C": 1}),
        ("Ben Green reached first on a dropped fly by cf, advanced to second (2-2 KBBF).", {"BIP": 1, "H": 0, "FB": 1, "LOC_CF": 1}),
        ("Smith struck out swinging, grounded out to c unassisted.", {"K": 1, "BIP": 0}),
        ("Max Tremblay reached on an error by Jackson Riedling (E4) (0-1 S).", {"BIP": 1, "GB": 1, "LOC_2B": 1}),
        ("Mason Shimkus out on batter's interference.", {"BIP": 1, "K": 0}),
        ("Mason Shimkus reached on a fielder's choice hit through the left side of the infield (0-1 K).", {"BIP": 1, "GB": 1}),
        ("Eric Bacon singled down the rf line; Jadyn McNealy advanced to third.", {"H": 1, "GB": 1, "LOC_RF": 1}),
        ("Quinn Johnson singled down the lf line; Ben Green advanced to second.", {"H": 1, "GB": 1, "LOC_LF": 1}),
        ("Isaac Hill flied out to cf, RBI SAC; Keenan Morris scored.", {"BIP": 1, "FB": 1, "BUNT": 0, "LOC_CF": 1}),
        ("Easton Ford reached on a fielding error by rf, advanced to second, RBI SAC.", {"BIP": 1, "BUNT": 0, "LOC_RF": 1}),
        ("Logan Rose singled to deep center field (2-1 BKB).", {"H": 1, "FB": 1, "LOC_CF": 1}),
    ],
)
def test_presto_lane_parity_wordings(line, expect):
    stats = aggregate_game_stats(process_game(f"Top of 1st\n{line}\n{FILLER}\n"))
    player = next(v for name, v in stats.items() if not name.startswith(("A,", "C,", "E,", "G,", "I,")))

    for key, value in expect.items():
        assert int(player.get(key) or 0) == value, (key, player.get(key))


@pytest.mark.parametrize(
    ("line", "event"),
    [
        ("#0 Ryan 2 reaches base due to a wild pitch third strike by the pitcher .", "strikeout"),
        ("#0 Ryan 9 is hit by the ball and called out.", "field_out"),
        (
            "#0 Ryan 9 grounds out on the throw third baseman to second baseman to first baseman . "
            "#0 Ryan 8 is forced out at second.",
            "ground_out",
        ),
        ("#0 Ryan 1 hits a hard fly ball for a Homerun!.", "home_run"),
    ],
)
def test_iscore_wordings_read_natively(line, event):
    from cleaners.iscore_cleaner import clean_iscore_text
    from language.reader import build_multi_platform_plate_appearance

    cleaned = clean_iscore_text(line)
    assert cleaned
    pa = build_multi_platform_plate_appearance(cleaned[0])
    assert pa.baseball_event.primary_event.value.startswith(event)


def test_more_statcrew_batter_verbs_and_short_first_names():
    from language.reader import build_multi_platform_plate_appearance

    assert build_multi_platform_plate_appearance("Chris Benavidez infield singled to third base (1-1 SB).").batter_name == "Chris Benavidez"
    assert build_multi_platform_plate_appearance("Kole Kinnison ground-rule doubled to left center.").batter_name == "Kole Kinnison"
    assert RosterMatcher(["Jose Griswold", "Caiden Hubbard"]).match("Joseph Griswold") == "Jose Griswold"
    assert RosterMatcher(["Jo Smith", "Joseph Smith"]).match("Joseph Smith") == "Joseph Smith"
