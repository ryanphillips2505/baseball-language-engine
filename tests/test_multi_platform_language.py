"""
Phrase-level coverage for the multi-platform reader.

One case per phrasing family per platform, taken from the shapes seen
in real MLB Gameday, ESPN, StatCrew-family (NCAA / Sidearm / Presto /
StatBroadcast) and iScore play-by-play. Player names are fictional.

Each case states what Opponent IQ needs from the play: the event, the
batter, the ball type (GB / FB / BUNT, only when the text says how the
ball was hit), the fielder location, and runner events.
"""

import pytest

from aggregators.game_stat_aggregator import aggregate_game_stats
from detectors.source_detector import SourceType, detect_source
from language.normalizer import normalize_play_text
from language.reader import build_multi_platform_plate_appearance
from pipeline.process_game import process_game


def read(text):
    pa = build_multi_platform_plate_appearance(text)
    event = pa.baseball_event.primary_event.value if pa.baseball_event else None
    runners = [(r.event_type, r.base, r.runner_name) for r in pa.runner_events]
    return {
        "event": event,
        "batter": pa.batter_name,
        "ball_type": pa.ball_type,
        "location": pa.location,
        "bip": pa.is_bip,
        "runners": runners,
    }


# (text, event, batter, ball_type, location)
BATTER_CASES = [
    # --- MLB Gameday -------------------------------------------------
    ("Sam Ortiz singles on a line drive to left fielder Al Cole.", "single", "Sam Ortiz", "FB", "LF"),
    ("Sam Ortiz grounds out, shortstop Ty Wells to first baseman Bo Hart.", "ground_out", "Sam Ortiz", "GB", "SS"),
    ("Sam Ortiz grounds out, pitcher Lee Park to first baseman Bo Hart.", "ground_out", "Sam Ortiz", "GB", "P"),
    ("Sam Ortiz grounds out softly, pitcher Lee Park to first baseman Bo Hart. Al Cole to 3rd.", "ground_out", "Sam Ortiz", "GB", "P"),
    ("Sam Ortiz flies out sharply to center fielder Jo Dunn.", "fly_out", "Sam Ortiz", "FB", "CF"),
    ("Sam Ortiz pops out to first baseman Bo Hart in foul territory.", "pop_out", "Sam Ortiz", "FB", "1B"),
    ("Sam Ortiz homers (12) on a fly ball to left center field.", "home_run", "Sam Ortiz", "FB", "LF"),
    ("Sam Ortiz hits a grand slam (3) to right center field. Al Cole scores. Bo Hart scores. Ty Wells scores.", "home_run", "Sam Ortiz", None, "RF"),
    ("Sam Ortiz hits a ground-rule double (6) on a line drive down the left-field line.", "double", "Sam Ortiz", "FB", "LF"),
    ("Sam Ortiz hits an inside-the-park home run (2) on a line drive to center field.", "home_run", "Sam Ortiz", "FB", "CF"),
    ("Sam Ortiz out on a sacrifice bunt, pitcher Lee Park to first baseman Bo Hart. Al Cole to 2nd.", "sac_bunt", "Sam Ortiz", "BUNT", "P"),
    ("Sam Ortiz out on a sacrifice fly to right fielder Jo Dunn. Al Cole scores.", "sac_fly", "Sam Ortiz", "FB", "RF"),
    ("Sam Ortiz lines into a double play, shortstop Ty Wells to second baseman Kai Moss. Al Cole out at 2nd.", "double_play", "Sam Ortiz", "FB", "SS"),
    ("Sam Ortiz lines into a force out, second baseman Kai Moss to shortstop Ty Wells. Al Cole out at 2nd.", "fielders_choice", "Sam Ortiz", "FB", "2B"),
    ("Sam Ortiz grounds into a triple play, third baseman Rey Diaz to second baseman Kai Moss to first baseman Bo Hart.", "double_play", "Sam Ortiz", "GB", "3B"),
    ("Sam Ortiz reaches on a throwing error by shortstop Ty Wells.", "error", "Sam Ortiz", None, "SS"),
    ("Sam Ortiz reaches on a missed catch error by first baseman Bo Hart.", "error", "Sam Ortiz", None, "1B"),
    ("Sam Ortiz bunt grounds out, catcher Max Ruiz to first baseman Bo Hart.", "ground_out", "Sam Ortiz", "BUNT", "C"),
    ("Sam Ortiz strikes out swinging, catcher Max Ruiz to first baseman Bo Hart.", "strikeout_swinging", "Sam Ortiz", None, None),
    ("Sam Ortiz called out on strikes.", "strikeout_looking", "Sam Ortiz", None, None),
    ("Sam Ortiz walks. Al Cole to 2nd.", "walk", "Sam Ortiz", None, None),
    ("Lee Park intentionally walks J.P. Ortiz.", "walk", "J.P. Ortiz", None, None),
    ("Lee Park intentionally walks Luis Vega Jr.", "walk", "Luis Vega Jr.", None, None),
    ("Sam Ortiz reaches on catcher interference by Max Ruiz. Sam Ortiz to 1st.", "catcher_interference", "Sam Ortiz", None, None),
    ("Angels challenged (tag play), call on the field was overturned: Sam Ortiz walks.", "walk", "Sam Ortiz", None, None),
    ("José Ramírez singles on a ground ball to right fielder Jo Dunn.", "single", "José Ramírez", "GB", "RF"),
    # --- ESPN generated ----------------------------------------------
    ("S. Ortiz grounded out to shortstop.", "ground_out", "S. Ortiz", "GB", "SS"),
    ("S. Ortiz flied out to center.", "fly_out", "S. Ortiz", "FB", "CF"),
    ("S. Ortiz fouled out to first.", "pop_out", "S. Ortiz", "FB", "1B"),
    ("S. Ortiz singled to shallow left, A. Cole scored.", "single", "S. Ortiz", None, "LF"),
    ("S. Ortiz tripled to deep center.", "triple", "S. Ortiz", None, "CF"),
    ("S. Ortiz walked, A. Cole to second.", "walk", "S. Ortiz", None, None),
    ("S. Ortiz grounded into fielder's choice to shortstop, A. Cole out at second.", "fielders_choice", "S. Ortiz", "GB", "SS"),
    ("S. Ortiz reached on bunt single to pitcher.", "single", "S. Ortiz", "BUNT", "P"),
    ("S. Ortiz hit a ground rule double to left.", "double", "S. Ortiz", None, "LF"),
    ("S. Ortiz safe at first on fielding error by second baseman K. Moss.", "error", "S. Ortiz", None, "2B"),
    ("S. Ortiz safe at second on error by shortstop T. Wells.", "error", "S. Ortiz", None, "SS"),
    ("S. Ortiz sacrified to first, A. Cole to third.", "sac_bunt", "S. Ortiz", "BUNT", "1B"),
    ("Jal. Ortiz flied out to left.", "fly_out", "Jal. Ortiz", "FB", "LF"),
    # --- StatCrew family (NCAA / Sidearm / Presto / StatBroadcast) ---
    ("Ortiz grounded out to ss (1-2 KBK).", "ground_out", "Ortiz", "GB", "SS"),
    ("Ortiz, Sam grounded out to 2b unassisted (0-0).", "ground_out", "Ortiz, Sam", "GB", "2B"),
    ("Ortiz,Sam popped up to 3b (2-0 BB).", "pop_out", "Ortiz,Sam", "FB", "3B"),
    ("ORTIZ, S. fouled out to c (0-1 K).", "pop_out", "ORTIZ, S.", "FB", "C"),
    ("Ortiz flied out to cf to left center (1-1 BK).", "fly_out", "Ortiz", "FB", "CF"),
    ("Ortiz lined out to p (0-0).", "line_out", "Ortiz", "FB", "P"),
    ("Ortiz singled up the middle (0-1 K).", "single", "Ortiz", None, "CF"),
    ("Ortiz singled through the left side, RBI (1-1 BK); Cole scored.", "single", "Ortiz", None, "LF"),
    ("Ortiz singled through the right side (0-0).", "single", "Ortiz", None, "RF"),
    ("Ortiz doubled down the lf line, 2 RBI (1-1 KB); Cole scored; Hart scored.", "double", "Ortiz", None, "LF"),
    ("Ortiz homered down the rf line, RBI (3-1 SBBB).", "home_run", "Ortiz", None, "RF"),
    ("Ortiz singled, bunt (1-0 B); Cole advanced to second.", "single", "Ortiz", "BUNT", None),
    ("Ortiz grounded out to p, SAC, bunt (0-0); Cole advanced to second.", "ground_out", "Ortiz", "BUNT", "P"),
    ("Ortiz out at first 1b to 2b, SAC, bunt (0-0); Cole advanced to second.", "sac_bunt", "Ortiz", "BUNT", "1B"),
    ("Ortiz out at first 1b to p (0-0).", "field_out", "Ortiz", None, "1B"),
    ("Ortiz reached on a fielder's choice (0-2); Cole out at second ss to 2b.", "fielders_choice", "Ortiz", None, "SS"),
    ("Ortiz reached on a throwing error by 3b (0-0).", "error", "Ortiz", None, "3B"),
    ("Ortiz reached on a muffed throw by 1b (3-2 BSFBBFF).", "error", "Ortiz", None, "1B"),
    ("Ortiz reached on catcher's interference (0-0).", "catcher_interference", "Ortiz", None, None),
    ("Ortiz grounded into double play ss to 2b to 1b (0-0); Cole out on the play.", "double_play", "Ortiz", "GB", "SS"),
    ("Ortiz lined into double play 1b unassisted (0-1); Cole out on the play.", "double_play", "Ortiz", "FB", "1B"),
    ("Ortiz struck out swinging, out at first c to 1b (3-2 SSBFBFBFS).", "strikeout_swinging", "Ortiz", None, None),
    ("Ortiz struck out, out at first c to 1b (0-0).", "strikeout", "Ortiz", None, None),
    ("Ortiz walked (3-1 BSBBB); Cole advanced to second.", "walk", "Ortiz", None, None),
    ("Ortiz intentionally walked.", "walk", "Ortiz", None, None),
    ("Ortiz hit by pitch (0-1 K); Cole advanced to second.", "hit_by_pitch", "Ortiz", None, None),
    ("Ortiz infield fly to ss (1-0 B).", "infield_fly", "Ortiz", "FB", "SS"),
    # --- iScore --------------------------------------------------------
    ("#7 Sam Ortiz hits a medium line drive for a single. #4 Al Cole advances to second.", "single", "Sam Ortiz", "FB", None),
    ("#7 Sam Ortiz grounds out . Unassisted out by first baseman .", "ground_out", "Sam Ortiz", "GB", "1B"),
    ("#7 Sam Ortiz bunts for an out to the pitcher on the throw pitcher to first baseman .", "ground_out", "Sam Ortiz", "BUNT", "P"),
    ("#7 Sam Ortiz hits a ground rule double.", "double", "Sam Ortiz", None, None),
    ("#7 Sam Ortiz is intentionally walked.", "walk", "Sam Ortiz", None, None),
    ("Ball 4. #7 Sam Ortiz is walked. #4 Al Cole advances to second.", "walk", "Sam Ortiz", None, None),
    ("#7 Sam Ortiz is hit by the pitch, goes to first.", "hit_by_pitch", "Sam Ortiz", None, None),
    ("#7 Sam Ortiz reaches base due to an error on the third baseman .", "error", "Sam Ortiz", None, "3B"),
]


@pytest.mark.parametrize("text, event, batter, ball_type, location", BATTER_CASES)
def test_batter_phrasing(text, event, batter, ball_type, location):
    reading = read(text)

    assert reading["event"] == event
    assert reading["batter"] == batter
    assert reading["ball_type"] == ball_type
    assert reading["location"] == location


# (text, expected runner events, expected primary event)
RUNNER_CASES = [
    ("Sal Ortiz steals (14) 2nd base.", [("SB", "2B", "Sal Ortiz")], "stolen_base"),
    ("Julio Rodríguez steals (3) 3rd base.", [("SB", "3B", "Julio Rodríguez")], "stolen_base"),
    ("Sal Ortiz caught stealing 2nd base, catcher Max Ruiz to shortstop Ty Wells.", [("CS", "2B", "Sal Ortiz")], "caught_stealing"),
    ("Sal Ortiz picked off and caught stealing 3rd base, catcher Max Ruiz to third baseman Rey Diaz.", [("CS", "3B", "Sal Ortiz")], "caught_stealing"),
    ("Pearson, Js. stole second.", [("SB", "2B", "Pearson, Js.")], "stolen_base"),
    ("R. Rigdon caught stealingsecond, catcher to shortstop.", [("CS", "2B", "R. Rigdon")], "caught_stealing"),
    ("Cole out at second c to ss, caught stealing.", [("CS", "2B", "Cole")], "caught_stealing"),
    ("C. Moss stole second, C. Moss safe at third on throwing error by catcher A. Ruiz.", [("SB", "2B", "C. Moss")], "stolen_base"),
    ("#12 Sam Ortiz steals second.", [("SB", "2B", "Sam Ortiz")], "stolen_base"),
    ("#3 Bo Li is caught stealing second.", [("CS", "2B", "Bo Li")], "caught_stealing"),
    ("Sal Ortiz steals (2) home.", [("SB", "HOME", "Sal Ortiz")], "stolen_base"),
]


@pytest.mark.parametrize("text, runners, event", RUNNER_CASES)
def test_runner_phrasing(text, runners, event):
    reading = read(text)

    assert reading["runners"] == runners
    assert reading["event"] == event
    assert reading["batter"] is None


def test_strikeout_with_runner_caught_stealing_credits_both():
    reading = read(
        "Bo Hart strikes out swinging and Al Cole caught stealing 2nd, catcher Max Ruiz to shortstop Ty Wells."
    )

    assert reading["event"] == "strikeout_swinging"
    assert reading["batter"] == "Bo Hart"
    assert reading["runners"] == [("CS", "2B", "Al Cole")]


def test_statcrew_pitch_sequence_becomes_swing_decisions():
    pa = build_multi_platform_plate_appearance("Ortiz flied out to cf (2-2 BKSFB).")

    assert [(p.count, p.outcome.value) for p in pa.pitches] == [
        ("0-0", "BALL"),
        ("1-0", "CALLED_STRIKE"),
        ("1-1", "SWING_MISS"),
        ("1-2", "FOUL"),
        ("1-2", "BALL"),
        ("2-2", "BIP"),
    ]


def test_statcrew_pitch_sequence_with_unknown_code_is_not_guessed():
    pa = build_multi_platform_plate_appearance("Ortiz walked (3-0 BBXB).")

    assert pa.pitches == []


def test_fouled_out_is_not_read_as_a_foul_pitch():
    pa = build_multi_platform_plate_appearance("S. Ortiz fouled out to first.")

    assert pa.pitches == []


@pytest.mark.parametrize(
    "text, expected",
    [
        ("grounded out to ss (1-2 KBK).", "grounded out to shortstop."),
        ("doubled down the lf line", "doubled to left field"),
        ("singled to shallow center", "singled to center"),
        ("C. Smith grounded out to p.", "C. Smith grounded out to pitcher."),
        ("game at 5 p.m. today", "game at 5 p.m. today"),
    ],
)
def test_normalizer_rewrites_aliases_only(text, expected):
    assert normalize_play_text(text) == expected


STATCREW_GAME = """
Top of 1st
Ortiz singled to left field (1-0 B).
Cole stole second.
Hart struck out swinging (1-2 KBS).
Moss grounded out to ss (0-0); Cole advanced to third.
Diaz walked (3-1 BBKBB).
Wells flied out to cf (0-1 K).
"""


def test_unlabeled_statcrew_text_is_read_as_college():
    assert detect_source(STATCREW_GAME) == SourceType.COLLEGE


def test_statcrew_game_end_to_end_stats():
    stats = aggregate_game_stats(process_game(STATCREW_GAME))

    assert stats["Ortiz"]["LOC_LF"] == 1
    assert stats["Ortiz"]["BIP"] == 1
    assert stats["Cole"]["SB"] == 1
    assert stats["Cole"]["SB-2B"] == 1
    assert stats["Hart"]["K"] == 1
    assert stats["Moss"]["GB-LOC_SS"] == 1
    assert stats["Diaz"]["BB"] == 1
    assert stats["Diaz"]["LOC_2B"] == 0
    assert stats["Wells"]["FB-LOC_CF"] == 1


def test_major_league_baseball_header_is_detected_as_mlb():
    text = "Major League Baseball\nSam Ortiz walks.\nBo Hart strikes out swinging.\n"

    assert detect_source(text) == SourceType.MLB


def test_gameday_strikeout_and_steal_keeps_both():
    text = (
        "Major League Baseball\n"
        "Bo Hart strikes out swinging. Al Cole steals (4) 2nd base.\n"
        "Lindor Ruiz steals (2) 3rd base. Sam Soto steals (5) 2nd base.\n"
    )

    stats = aggregate_game_stats(process_game(text))

    assert stats["Bo Hart"]["K"] == 1
    assert stats["Bo Hart"]["SB"] == 0
    assert stats["Al Cole"]["SB"] == 1
    assert stats["Lindor Ruiz"]["SB-3B"] == 1
    assert stats["Sam Soto"]["SB-2B"] == 1
