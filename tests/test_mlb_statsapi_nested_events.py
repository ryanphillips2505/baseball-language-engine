from __future__ import annotations

from pathlib import Path

from cleaners.mlb_statsapi_cleaner import clean_mlb_statsapi_timeline_text
from models.timeline_block import GameEventBlock, PlateAppearanceBlock
from pipeline.process_game import process_game


MARINERS = Path(
    "samples/mlb/statsapi/raw/mlb_redsox_mariners_2026_06_20_gamepk823126.live.json"
)
ANGELS = Path(
    "samples/mlb/statsapi/raw/mlb_angels_athletics_2026_06_20_gamepk824988.live.json"
)


def test_nested_stolen_base_and_wild_pitch_surface_on_timeline():
    blocks = clean_mlb_statsapi_timeline_text(MARINERS.read_text(encoding="utf-8"))

    runner_events = [
        block
        for block in blocks
        if isinstance(block, GameEventBlock)
        and not (block.metadata or {}).get("administrative")
    ]
    runner_types = [block.event_type for block in runner_events]

    assert runner_types.count("stolen_base") == 4
    assert runner_types.count("wild_pitch") == 2
    assert runner_types.count("caught_stealing") == 2

    assert any(
        "Masataka Yoshida steals" in block.raw_text for block in runner_events
    )
    assert any(
        "Wild pitch by pitcher Emerson Hancock" in block.raw_text
        for block in runner_events
    )
    assert any(
        "Julio Rodríguez caught stealing 3rd" in block.raw_text
        for block in runner_events
    )


def test_nested_substitutions_are_quarantined_admin_events():
    blocks = clean_mlb_statsapi_timeline_text(MARINERS.read_text(encoding="utf-8"))

    admin_blocks = [
        block
        for block in blocks
        if isinstance(block, GameEventBlock)
        and (block.metadata or {}).get("administrative")
    ]
    admin_types = [block.event_type for block in admin_blocks]

    assert admin_types.count("pitching_change") == 7
    assert admin_types.count("offensive_substitution") == 2
    assert admin_types.count("defensive_substitution") == 1
    assert admin_types.count("defensive_switch") + admin_types.count(
        "defensive_assignment"
    ) == 3

    assert any(
        "Pitching Change: José A. Ferrer replaces Emerson Hancock."
        in block.raw_text
        for block in admin_blocks
    )
    assert not any(
        pa.batter_name and "Pitching Change" in pa.batter_name
        for pa in process_game(MARINERS.read_text(encoding="utf-8")).plate_appearances
    )


def test_nested_events_preserve_plate_appearance_count():
    raw = MARINERS.read_text(encoding="utf-8")
    blocks = clean_mlb_statsapi_timeline_text(raw)
    game = process_game(raw)

    pa_blocks = [
        block for block in blocks if isinstance(block, PlateAppearanceBlock)
    ]
    assert len(pa_blocks) == 70
    assert len(game.plate_appearances) == 70

    # Nested actions expand the timeline beyond result descriptions alone.
    assert len(blocks) > 71


def test_nested_events_keep_chronology_before_result_play():
    blocks = clean_mlb_statsapi_timeline_text(MARINERS.read_text(encoding="utf-8"))

    # During Wilyer Abreu's walk, Yoshida steals before the walk result.
    texts = [block.raw_text for block in blocks]
    steal_idx = next(
        i for i, text in enumerate(texts) if "Masataka Yoshida steals" in text
    )
    walk_idx = next(
        i for i, text in enumerate(texts) if text.startswith("Wilyer Abreu walks")
    )
    assert steal_idx < walk_idx


def test_angels_nested_admin_does_not_create_false_pas():
    game = process_game(ANGELS.read_text(encoding="utf-8"))
    assert len(game.plate_appearances) == 79
    assert not any(
        pa.batter_name and "Pitching Change" in (pa.batter_name or "")
        for pa in game.plate_appearances
    )
