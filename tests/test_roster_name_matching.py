import pytest

from adapters.legacy_process_game_text import process_game_text
from language.names import RosterMatcher, resolve_player_stats


ROSTER = [
    "Lawson DeVault",
    "James Wilson",
    "Jalen Flores",
    "Josh Pearson",
    "Jake Pearson",
    "José Ramírez",
    "Juan De La Cruz",
    "Luis Robert Jr.",
    "Cody Thomas",
    "Chris Thomas",
    "Anthony Lazits",
]


@pytest.mark.parametrize(
    "pbp_name, roster_name",
    [
        ("Lawson DeVault", "Lawson DeVault"),
        ("L. Devault", "Lawson DeVault"),
        ("L Devault", "Lawson DeVault"),
        ("Devault, L.", "Lawson DeVault"),
        ("DeVault,Lawson", "Lawson DeVault"),
        ("DEVAULT", "Lawson DeVault"),
        ("#12 Lawson DeVault", "Lawson DeVault"),
        ("Jal. Flores", "Jalen Flores"),
        ("Pearson, Js.", "Josh Pearson"),
        ("Jose Ramirez", "José Ramírez"),
        ("J. De La Cruz", "Juan De La Cruz"),
        ("Luis Robert", "Luis Robert Jr."),
        ("Ch. Thomas", "Chris Thomas"),
        ("Lazits,Anto", "Anthony Lazits"),
    ],
)
def test_play_by_play_names_resolve_to_roster(pbp_name, roster_name):
    assert RosterMatcher(ROSTER).match(pbp_name) == roster_name


@pytest.mark.parametrize("pbp_name", ["Pearson", "J Pearson", "Thomas", "C. Thomas", "Nobody Here", ""])
def test_ambiguous_or_unknown_names_are_not_guessed(pbp_name):
    assert RosterMatcher(ROSTER).match(pbp_name) is None


def test_spellings_of_one_player_are_merged():
    stats = {
        "L. Devault": {"GP": 1, "BB": 1, "SB": 0},
        "Devault, L.": {"GP": 1, "BB": 0, "SB": 1},
        "Visitor Guy": {"GP": 1, "BB": 2, "SB": 0},
    }

    resolved, unmatched = resolve_player_stats(stats, ROSTER)

    assert resolved == {"Lawson DeVault": {"GP": 1, "BB": 1, "SB": 1}}
    assert unmatched == ["Visitor Guy"]


def test_opponent_iq_adapter_applies_name_recognition():
    raw = """
Top of 1st
L. Devault walked (3-1 BBKBB).
L. Devault stole second.
J. Wilson singled to left field (0-0).
X. Visitor struck out swinging (0-2 KS).
"""

    team, players = process_game_text(raw, roster_names={"Lawson DeVault", "James Wilson"})

    assert set(players) == {"Lawson DeVault", "James Wilson"}
    assert players["Lawson DeVault"]["BB"] == 1
    assert players["Lawson DeVault"]["SB"] == 1
    assert players["James Wilson"]["BIP"] == 1
    assert players["James Wilson"]["LF"] == 1
