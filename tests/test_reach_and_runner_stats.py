"""
H / ROE / FC / PR / CR for non-GameChanger games, using the Opponent IQ
Legacy definitions. GameChanger output must not gain these keys.
"""

from adapters.opponent_iq_engine_adapter import process_raw_text_to_opponent_iq_game
from language.substitutions import extract_runner_entries
from pipeline.process_game import process_game

COLLEGE_GAME = """College baseball play-by-play
Ortiz singled to left field (1-0 B).
Hart reached on a throwing error by ss (0-0).
Moss reached on a fielder's choice (0-2); Ortiz out at second ss to 2b.
Diaz homered to left field, RBI (0-0).
Wells grounded into double play ss to 2b to 1b (0-0); Moss out on the play.
J. Lee pinch ran for Hart.
Kim courtesy ran for Diaz.
"""


def test_college_reach_and_runner_stats():
    team, players = process_raw_text_to_opponent_iq_game(COLLEGE_GAME)

    assert players["Ortiz"]["H"] == 1
    assert players["Diaz"]["H"] == 1
    assert players["Hart"]["ROE"] == 1
    assert players["Moss"]["FC"] == 1
    assert players["Wells"]["FC"] == 0
    assert players["J. Lee"]["PR"] == 1
    assert players["Kim"]["CR"] == 1
    assert {key: team[key] for key in ("H", "ROE", "FC", "PR", "CR")} == {
        "H": 2, "ROE": 1, "FC": 1, "PR": 1, "CR": 1,
    }


def test_gamechanger_output_has_no_new_keys():
    raw = "All Plays\nTop 1st\nJohn Smith singles on a line drive to center fielder.\n"

    _team, players = process_raw_text_to_opponent_iq_game(raw)

    assert process_game(raw).source is None
    assert not {"H", "ROE", "FC", "PR", "CR"} & set(players["John Smith"])


def test_runner_entry_wording_per_platform():
    text = "\n".join([
        "Lineup changed: Pinch runner Jake Lee in for catcher Bo Hart",
        "Courtesy runner Sam Ortiz in for Al Cole",
        "Offensive Substitution: Pinch-runner Esteury Ruiz replaces Graham Pauley.",
        "J. Hudson pinch ran for J. Wills.",
        "Kim courtesy ran for Diaz.",
        "T. Lane ran for B. Hart.",
        "Offensive Substitution: Pinch-hitter Joc Pederson replaces Justin Foscue.",
    ])

    assert extract_runner_entries(text) == [
        ("Jake Lee", "PR"),
        ("Sam Ortiz", "CR"),
        ("Esteury Ruiz", "PR"),
        ("J. Hudson", "PR"),
        ("Kim", "CR"),
        ("T. Lane", "PR"),
    ]
