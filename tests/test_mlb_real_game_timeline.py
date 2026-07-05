from pathlib import Path

from assemblers.game_builder import build_game
from cleaners.mlb_timeline_cleaner import clean_mlb_timeline_text
from models.timeline_block import TimelineBlockType


def test_real_mlb_game_timeline_separates_runner_only_events():

    sample = Path("samples/mlb/validation/red_sox_angels_2026_07_04.txt")

    blocks = clean_mlb_timeline_text(
        sample.read_text(encoding="utf-8")
    )

    game = build_game(blocks)

    events = [
        block
        for block in game.timeline.blocks
        if block.block_type == TimelineBlockType.GAME_EVENT
    ]

    assert len(game.timeline) == 75
    assert len(game.plate_appearances) == 72

    assert [event.event_type for event in events] == [
        "stolen_base",
        "wild_pitch",
        "wild_pitch",
    ]

    assert events[0].metadata["game_event"].base == "2nd"
