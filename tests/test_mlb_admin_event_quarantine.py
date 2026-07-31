from pathlib import Path

from cleaners.mlb_admin_classifier import classify_mlb_admin_line
from cleaners.mlb_timeline_cleaner import clean_mlb_timeline_text
from models.timeline_block import GameEventBlock, PlateAppearanceBlock, TimelineBlockType
from pipeline.process_game import process_game


SAMPLE = Path("samples/mlb/validation/red_sox_angels_2026_07_04.txt")


def test_classify_pitching_change_and_defensive_substitution():
    assert (
        classify_mlb_admin_line(
            "Pitching Change: José Fermin replaces Reid Detmers."
        )
        == "pitching_change"
    )
    assert (
        classify_mlb_admin_line(
            "Defensive Substitution: Tyler Heineman replaces catcher "
            "Logan O'Hoppe, batting 9th, playing catcher."
        )
        == "defensive_substitution"
    )
    assert classify_mlb_admin_line("Injury Delay.") == "injury_delay"
    assert (
        classify_mlb_admin_line("Ball 1 overturned after ABS challenge")
        == "abs_review"
    )


def test_challenge_final_call_lines_are_not_admin_quarantine():
    text = (
        "Shea Langeliers challenged (pitch result), call on the field was "
        "overturned: Nolan Schanuel called out on strikes."
    )
    assert classify_mlb_admin_line(text) is None


def test_admin_lines_are_quarantined_not_plate_appearances():
    raw = """
Major League Baseball
Pitching Substitution
Pitching Change: José Fermin replaces Reid Detmers.
Nate Eaton strikes out swinging. 1 Out
Injury Delay.
Ceddanne Rafaela singles on a line drive to right fielder Jo Adell.
"""
    blocks = clean_mlb_timeline_text(raw)

    assert [block.block_type for block in blocks] == [
        TimelineBlockType.GAME_EVENT,
        TimelineBlockType.GAME_EVENT,
        TimelineBlockType.PLATE_APPEARANCE,
        TimelineBlockType.GAME_EVENT,
        TimelineBlockType.PLATE_APPEARANCE,
    ]
    assert blocks[0].event_type == "pitching_change"
    assert blocks[0].metadata.get("administrative") is True
    assert blocks[1].event_type == "pitching_change"
    assert isinstance(blocks[2], PlateAppearanceBlock)
    assert blocks[3].event_type == "injury_delay"
    assert "strikes out swinging" in blocks[2].raw_text


def test_red_sox_angels_fixture_quarantines_admin_without_changing_pa_count():
    raw = SAMPLE.read_text(encoding="utf-8")
    blocks = clean_mlb_timeline_text(raw)

    admin_blocks = [
        block
        for block in blocks
        if isinstance(block, GameEventBlock)
        and block.metadata.get("administrative")
    ]
    pa_blocks = [
        block for block in blocks if isinstance(block, PlateAppearanceBlock)
    ]
    runner_blocks = [
        block
        for block in blocks
        if isinstance(block, GameEventBlock)
        and not block.metadata.get("administrative")
    ]

    assert len(admin_blocks) == 18
    assert len(pa_blocks) == 73
    assert [block.event_type for block in runner_blocks] == [
        "stolen_base",
        "wild_pitch",
        "wild_pitch",
    ]

    game = process_game(raw)
    assert len(game.plate_appearances) == 73
    assert not any(
        pa.batter_name and "Pitching Change" in pa.batter_name
        for pa in game.plate_appearances
    )
