from pathlib import Path

from cleaners.mlb_admin_classifier import classify_mlb_admin_line
from cleaners.mlb_cleaner import clean_mlb_text
from cleaners.mlb_timeline_cleaner import clean_mlb_timeline_text
from models.timeline_block import GameEventBlock, PlateAppearanceBlock
from models.types import EventType
from pipeline.process_game import process_game


SAMPLE = Path("samples/mlb/validation/redsox_athletics_2026_07_30.txt")


def test_ball_is_overturned_after_abs_is_admin_review():
    text = "Ball 1 is overturned after ABS challenge"
    assert classify_mlb_admin_line(text) == "abs_review"


def test_strikes_out_after_abs_caption_is_rejected():
    assert clean_mlb_text("Colby Thomas strikes out after ABS challenge") == []


def test_redsox_athletics_gameday_core_understanding():
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

    assert len(pa_blocks) == 74
    assert len(game.plate_appearances) == 74
    assert [block.event_type for block in runner_blocks] == ["stolen_base"]
    assert any(block.event_type == "abs_review" for block in admin_blocks)
    assert not any(
        pa.batter_name is None or pa.baseball_event is None
        for pa in game.plate_appearances
    )

    assert any(
        pa.batter_name == "Caleb Durbin"
        and pa.baseball_event
        and pa.baseball_event.primary_event == EventType.SAC_BUNT
        for pa in game.plate_appearances
    )
    assert any(
        pa.batter_name == "Carlos Cortes"
        and pa.baseball_event
        and pa.baseball_event.primary_event == EventType.SAC_FLY
        for pa in game.plate_appearances
    )
    assert any(
        pa.batter_name == "Wilyer Abreu"
        and pa.baseball_event
        and pa.baseball_event.primary_event == EventType.HOME_RUN
        for pa in game.plate_appearances
    )
    assert any(
        pa.batter_name == "Willson Contreras"
        and pa.baseball_event
        and pa.baseball_event.primary_event == EventType.HOME_RUN
        for pa in game.plate_appearances
    )
    assert any(
        pa.batter_name == "Nick Kurtz"
        and pa.baseball_event
        and pa.baseball_event.primary_event == EventType.ERROR
        for pa in game.plate_appearances
    )

    colby = [
        pa
        for pa in game.plate_appearances
        if pa.batter_name == "Colby Thomas"
    ]
    assert len(colby) == 1
    assert colby[0].baseball_event.primary_event == EventType.STRIKEOUT_LOOKING
