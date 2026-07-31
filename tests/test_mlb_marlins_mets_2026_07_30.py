from pathlib import Path

from extractors.player_extractor import extract_batter_name
from cleaners.mlb_timeline_cleaner import clean_mlb_timeline_text
from models.timeline_block import GameEventBlock, PlateAppearanceBlock
from models.types import EventType
from pipeline.process_game import process_game


SAMPLE = Path("samples/mlb/validation/marlins_mets_2026_07_30.txt")


def test_out_on_sacrifice_bunt_assigns_batter():
    text = (
        "Xavier Edwards out on a sacrifice bunt, pitcher Nolan McLean to "
        "first baseman Brett Baty. Liam Hicks to 2nd. 1 Out"
    )
    assert extract_batter_name(text) == "Xavier Edwards"


def test_challenge_upheld_picks_off_is_pickoff_game_event():
    text = (
        "Marlins challenged (tag play), call on the field was upheld: "
        "pitcher Nolan McLean picks off Graham Pauley at 1st on throw to "
        "first baseman Brett Baty. 3 Outs"
    )
    blocks = clean_mlb_timeline_text(text)
    assert len(blocks) == 1
    assert isinstance(blocks[0], GameEventBlock)
    assert blocks[0].event_type == "pickoff"
    assert "picks off Graham Pauley" in blocks[0].raw_text


def test_throwing_error_on_pickoff_attempt_is_game_event_not_pa():
    text = "Throwing error by pitcher Nolan McLean on the pickoff attempt."
    blocks = clean_mlb_timeline_text(text)
    assert len(blocks) == 1
    assert isinstance(blocks[0], GameEventBlock)
    assert blocks[0].event_type == "pickoff_error"


def test_marlins_mets_gameday_core_understanding():
    raw = SAMPLE.read_text(encoding="utf-8")
    blocks = clean_mlb_timeline_text(raw)
    game = process_game(raw)

    pa_blocks = [
        block for block in blocks if isinstance(block, PlateAppearanceBlock)
    ]
    admin_blocks = [
        block
        for block in blocks
        if isinstance(block, GameEventBlock)
        and (block.metadata or {}).get("administrative")
    ]
    runner_blocks = [
        block
        for block in blocks
        if isinstance(block, GameEventBlock)
        and not (block.metadata or {}).get("administrative")
    ]

    assert len(pa_blocks) == 68
    assert len(game.plate_appearances) == 68

    assert [block.event_type for block in runner_blocks] == [
        "pickoff",
        "pickoff_error",
        "stolen_base",
        "passed_ball",
        "stolen_base",
    ]
    assert any("picks off Graham Pauley" in block.raw_text for block in runner_blocks)
    assert any(
        "Throwing error by pitcher Nolan McLean on the pickoff attempt"
        in block.raw_text
        for block in runner_blocks
    )

    assert len(admin_blocks) >= 10
    assert not any(
        pa.batter_name is None and pa.baseball_event is None
        for pa in game.plate_appearances
    )

    sac = [
        pa
        for pa in game.plate_appearances
        if pa.batter_name == "Xavier Edwards"
        and pa.baseball_event
        and pa.baseball_event.primary_event == EventType.SAC_BUNT
    ]
    assert len(sac) == 1

    assert any(
        pa.batter_name == "Kyle Stowers"
        and pa.baseball_event
        and pa.baseball_event.primary_event == EventType.HOME_RUN
        for pa in game.plate_appearances
    )
    assert any(
        pa.batter_name == "Jakob Marsee"
        and pa.baseball_event
        and pa.baseball_event.primary_event == EventType.HOME_RUN
        for pa in game.plate_appearances
    )
    assert any(
        pa.batter_name == "Luis Robert Jr."
        and pa.baseball_event
        and pa.baseball_event.primary_event == EventType.ERROR
        for pa in game.plate_appearances
    )
    assert any(
        pa.batter_name == "Joe Mack"
        and pa.baseball_event
        and pa.baseball_event.primary_event == EventType.DOUBLE_PLAY
        for pa in game.plate_appearances
    )
    assert any(
        pa.batter_name == "Carson Benge"
        and pa.baseball_event
        and pa.baseball_event.primary_event == EventType.STRIKEOUT_LOOKING
        for pa in game.plate_appearances
    )
