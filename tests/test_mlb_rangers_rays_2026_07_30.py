from pathlib import Path

from extractors.player_extractor import extract_batter_name
from models.types import EventType
from pipeline.process_game import process_game
from cleaners.mlb_timeline_cleaner import clean_mlb_timeline_text
from models.timeline_block import GameEventBlock, PlateAppearanceBlock


SAMPLE = Path("samples/mlb/validation/rangers_rays_2026_07_30.txt")


def test_umpire_reviewed_upheld_assigns_final_call_batter():
    text = (
        "Umpire reviewed (home run), call on the field was upheld: "
        "Junior Caminero flies out sharply to center fielder Cam Cauley. 3 Outs"
    )
    assert extract_batter_name(text) == "Junior Caminero"


def test_intentional_walk_assigns_batter_not_pitcher():
    text = (
        "Marco Gonzales intentionally walks Junior Caminero. "
        "Yandy Díaz to 3rd. Jonathan Aranda to 2nd."
    )
    assert extract_batter_name(text) == "Junior Caminero"


def test_rangers_rays_gameday_core_understanding():
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

    assert len(pa_blocks) == 71
    assert len(game.plate_appearances) == 71
    assert len(runner_blocks) == 3
    assert [block.event_type for block in runner_blocks] == [
        "stolen_base",
        "stolen_base",
        "stolen_base",
    ]
    assert len(admin_blocks) >= 20
    assert not any(
        pa.batter_name
        and any(
            marker in pa.batter_name
            for marker in (
                "Pitching Change",
                "Offensive Substitution",
                "Defensive switch",
                "Umpire reviewed",
                "Marco Gonzales",
            )
        )
        for pa in game.plate_appearances
    )

    caminero_fly = [
        pa
        for pa in game.plate_appearances
        if pa.batter_name == "Junior Caminero"
        and pa.baseball_event
        and pa.baseball_event.primary_event == EventType.FLY_OUT
    ]
    assert caminero_fly

    caminero_ibb = [
        pa
        for pa in game.plate_appearances
        if pa.batter_name == "Junior Caminero"
        and pa.baseball_event
        and pa.baseball_event.primary_event == EventType.WALK
    ]
    assert len(caminero_ibb) == 1

    assert any(
        pa.batter_name == "Joc Pederson"
        and pa.baseball_event
        and pa.baseball_event.primary_event == EventType.FIELDERS_CHOICE
        for pa in game.plate_appearances
    )
    assert any(
        pa.batter_name == "Jonny DeLuca"
        and pa.baseball_event
        and pa.baseball_event.primary_event == EventType.HOME_RUN
        for pa in game.plate_appearances
    )
    assert any(
        pa.batter_name == "Cedric Mullins"
        and pa.baseball_event
        and pa.baseball_event.primary_event == EventType.HOME_RUN
        for pa in game.plate_appearances
    )

    # Challenge final calls keep the actual batter/outcome.
    assert any(
        pa.batter_name == "Jonathan Aranda"
        and pa.baseball_event
        and pa.baseball_event.primary_event == EventType.STRIKEOUT_LOOKING
        for pa in game.plate_appearances
    )
    assert any(
        pa.batter_name == "Wyatt Langford"
        and pa.baseball_event
        and pa.baseball_event.primary_event == EventType.STRIKEOUT_LOOKING
        for pa in game.plate_appearances
    )
    assert any(
        pa.batter_name == "Nicky Lopez"
        and pa.baseball_event
        and pa.baseball_event.primary_event == EventType.WALK
        for pa in game.plate_appearances
    )
