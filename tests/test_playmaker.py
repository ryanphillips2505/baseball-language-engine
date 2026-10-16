"""PlayMaker game pages pasted as text."""

from pathlib import Path

from cleaners.playmaker_cleaner import clean_playmaker_text, looks_like_playmaker_text
from detectors.source_detector import SourceType, detect_source
from language.names import RosterMatcher, parse_name
from tools.language_audit.playmaker_parity import batting_boxes, score_game

SAMPLE = Path(__file__).resolve().parents[1] / "samples" / "playmaker" / "raw" / "pm_leones_aguilas.txt"


def _text() -> str:
    return SAMPLE.read_text(encoding="utf-8")


def test_playmaker_page_is_detected():
    assert detect_source(_text()) == SourceType.PLAYMAKER


def test_plays_come_out_in_game_order_without_box_or_summary():
    blocks = clean_playmaker_text(_text())

    assert len(blocks) == 76
    assert blocks[0].startswith("Line Out\nBrainer Bonaci lined out to left field")
    assert blocks[-1].startswith("Fielder's Choice\nMarvin Alcántara hit into a fielder's choice")
    assert not any("BATTING" in block or "—" in block for block in blocks)


def test_sample_matches_both_batting_boxes():
    source, checks, errors, misses = score_game(_text())

    assert source == "playmaker"
    assert checks == 66
    assert errors == 0, misses


def test_box_parser_reads_rows_without_a_position():
    boxes = batting_boxes(_text())

    assert len(boxes) == 2
    assert boxes[1]["rows"]["Y. Bucce"] == {"AB": 5, "R": 1, "H": 1, "RBI": 0, "BB": 0, "K": 2}
    assert boxes[1]["totals"][:6] == [29, 8, 6, 7, 10, 11]


def test_initial_box_names_match_full_play_names():
    assert RosterMatcher(["V. Arias", "A. Arteaga"]).match("Victor Arias") == "V. Arias"
    assert parse_name("V. Arias").first == "v"
    assert parse_name("Ken Griffey III").last == "griffey"


def test_gamechanger_text_is_never_playmaker():
    gc = "Top 1st - Wildcats\nGround Out\nIn play.\nJ Smith grounds out to shortstop.\n" * 6
    assert not looks_like_playmaker_text(gc)


def test_suffix_only_after_comma_is_not_a_first_name():
    assert parse_name("Stroemer, Jr").first == ""
    assert RosterMatcher(["Paul Stroemer Jr."]).match("Stroemer, Jr") == "Paul Stroemer Jr."


def test_same_name_players_split_by_suffix_or_nickname():
    m = RosterMatcher(["L. Ramírez jr (Luis Jr)", "L. Ramirez (Luis)"])

    assert m.match("Luis angel Ramírez jr (Luis Jr)") == "L. Ramírez jr (Luis Jr)"
    assert m.match("Luis Norberto Ramirez (Luis)") == "L. Ramirez (Luis)"


def test_positions_typed_into_names_are_ignored():
    m = RosterMatcher(["C. Cruz 1b", "E. Luevano Picher", "J. Luevano Cacher"])

    assert m.match("Carlos Cruz 1b") == "C. Cruz 1b"
    assert m.match("Eduardo Luevano Picher") == "E. Luevano Picher"
    assert clean_playmaker_text(
        "Top 1st\nWalk\nCarlos Cruz 1b walked\nWalk\nRaul Jaime SS walked\n" * 1
    )[0].endswith("Carlos Cruz walked")


def test_reached_on_error_label_overrules_a_stale_single_sentence():
    from language.reader import build_multi_platform_plate_appearance

    pa = build_multi_platform_plate_appearance(
        "Reached on Error\nGavin Gonzalez singled to short center field"
    )
    assert pa.baseball_event.primary_event.value == "error"
