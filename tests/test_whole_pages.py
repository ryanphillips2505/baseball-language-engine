"""Whole SIDEARM / PrestoSports box-score pages pasted as text."""

from aggregators.game_stat_aggregator import aggregate_game_stats
from detectors.source_detector import (
    SourceType,
    detect_source,
    detect_source_with_language_fallbacks,
)
from language.names import RosterMatcher
from language.pages import extract_statcrew_plays, looks_like_statcrew_page
from pipeline.process_game import process_game


# SIDEARM: a scoring summary, "All Innings", then the same innings again
# under per-inning tabs.
SIDEARM_PAGE = """Oklahoma 5, Kansas 2
Scoring Summary
Inning\tPlay\tKU\tOU
1st\tGambill, T. homered to left field (1-0 B). 0 1
Play By Play
All Innings
Kansas - Top of 1st
Smith, J. struck out swinging (1-2 BKS). 0 0
Brock,Brendan singled to left (0-0). 0 0
Brock,Brendan stole second base. 0 0
Jones, K. grounded out to ss (0-0). 0 0
Lee, M. flied out to cf (2-1 BBK). 0 0
0 Runs, 1 Hits, 0 Errors, 1 LOB
Oklahoma - Bottom of 1st
Gambill, T. homered to left field (1-0 B). 0 1
Willits, J. walked (3-1 BBBKB). 0 1
Moutzouridi lined out to 2b (0-0). 0 1
Catalano, M. struck out looking (2-2 BKBK). 0 1
Wells, D. grounded out to 3b (0-0). 0 1
1 Runs, 1 Hits, 0 Errors, 1 LOB
1st
Kansas - Top of 1st
Smith, J. struck out swinging (1-2 BKS). 0 0
Brock,Brendan singled to left (0-0). 0 0
Brock,Brendan stole second base. 0 0
Jones, K. grounded out to ss (0-0). 0 0
Lee, M. flied out to cf (2-1 BBK). 0 0
Oklahoma - Bottom of 1st
Gambill, T. homered to left field (1-0 B). 0 1
Willits, J. walked (3-1 BBBKB). 0 1
Moutzouridi lined out to 2b (0-0). 0 1
Catalano, M. struck out looking (2-2 BKBK). 0 1
Wells, D. grounded out to 3b (0-0). 0 1
1 Runs, 1 Hits, 0 Errors, 1 LOB
Box Score
"""

# PrestoSports page scored with GameChanger-style wording.
PRESTO_PRESENT_TENSE_PAGE = """Top of 1st
Inning
Smith is hit by pitch, Whiting pitching
DeVault strikes out looking, Whiting pitching
(1 out)
De La Rosa lines out to shortstop Daclan
(2 out)
Webb pops out to first baseman Hatley
(3 out)
Bottom of 1st
Inning
Salazar Mata singles on a ground ball to left fielder Fernandez
Fernandez strikes out swinging, Kimble pitching
(1 out)
Cole grounds out to second baseman Webb
(2 out)
Owens flies out to center fielder Smith
(3 out)
"""

GAMECHANGER_TEXT = """Top 1st - Wildcats
Ball 1
Strike 1 looking
In play.
J Smith grounds out to shortstop, Pitcher pitching.
Bottom 1st - Tigers
Strike 1 swinging
Ball 1
J Doe singles on a line drive to left fielder.
"""


def test_extractor_keeps_each_half_inning_once():
    plays = extract_statcrew_plays(SIDEARM_PAGE).splitlines()

    assert plays.count("Gambill, T. homered to left field (1-0 B). 0 1") == 1
    assert plays.count("Smith, J. struck out swinging (1-2 BKS). 0 0") == 1
    assert len(plays) == 10


def test_plain_play_by_play_is_unchanged():
    text = "Smith, J. struck out swinging.\nJones, K. singled to left."
    assert extract_statcrew_plays(text) == text


def test_sidearm_page_is_read_as_college_once():
    assert detect_source_with_language_fallbacks(SIDEARM_PAGE) == SourceType.COLLEGE

    stats = aggregate_game_stats(process_game(SIDEARM_PAGE))
    gambill = next(v for k, v in stats.items() if k.startswith("Gambill"))
    assert gambill["HR"] == 1
    assert gambill["H"] == 1
    assert stats["Brock,Brendan"]["SB"] == 1


def test_presto_present_tense_page_is_recognized_by_out_markers():
    assert looks_like_statcrew_page(PRESTO_PRESENT_TENSE_PAGE)
    assert detect_source_with_language_fallbacks(PRESTO_PRESENT_TENSE_PAGE) == SourceType.COLLEGE


def test_gamechanger_structure_vetoes_the_page_recognizer():
    assert not looks_like_statcrew_page(GAMECHANGER_TEXT)
    assert not looks_like_statcrew_page(GAMECHANGER_TEXT + PRESTO_PRESENT_TENSE_PAGE)
    assert detect_source_with_language_fallbacks(GAMECHANGER_TEXT) == detect_source(GAMECHANGER_TEXT)


def test_surname_fallbacks_are_unique_only():
    matcher = RosterMatcher([
        "Pj Moutzouridis",
        "Johnson, Camden",
        "Johnson, Cameron",
        "Gabriel Salazar",
        "Jacob De La Rosa",
        "Tom Hernandez",
        "Tim Hernandezz",
    ])

    assert matcher.match("Moutzouridi") == "Pj Moutzouridis"
    assert matcher.match("De La Rosa") == "Jacob De La Rosa"
    # Guesses stay unmatched: double surnames, word-boundary cuts, and
    # trailing-token fits ("Hao-Yu Lee" is not "Yu Lee").
    assert matcher.match("Salazar Mata") is None
    assert RosterMatcher(["Al Martinez-Smith"]).match("Martinez") is None
    assert RosterMatcher(["Yu Lee"]).match("Hao-Yu Lee") is None
    assert RosterMatcher(["Caught Stealing"]).match("Pickoff Caught Stealing") is None
    # Ambiguous: flagged (unmatched), never guessed.
    assert matcher.match("Johnson, C") is None
    assert matcher.match("Hernande") is None
    assert matcher.match("Moutz") is None


def test_sidearm_out_caught_stealing_wording():
    text = SIDEARM_PAGE.replace(
        "Brock,Brendan stole second base. 0 0",
        "Brock,Brendan out caught stealing at second base, c to ss. 0 0",
    )
    stats = aggregate_game_stats(process_game(text))
    assert stats["Brock,Brendan"]["CS"] == 1
    assert stats["Brock,Brendan"]["SB"] == 0
