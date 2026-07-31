from pathlib import Path

from assemblers.game_builder import build_game
from cleaners.mlb_timeline_cleaner import clean_mlb_timeline_text
from models.timeline_block import TimelineBlockType


def test_real_mlb_game_timeline_event_context():

    sample = Path("samples/mlb/validation/red_sox_angels_2026_07_04.txt")

    blocks = clean_mlb_timeline_text(
        sample.read_text(encoding="utf-8")
    )

    game = build_game(blocks)

    events = [
        block.metadata["game_event"]
        for block in game.timeline.blocks
        if block.block_type == TimelineBlockType.GAME_EVENT
        and not (block.metadata or {}).get("administrative")
    ]

    assert len(events) == 3

    assert events[0].event_type == "stolen_base"
    assert events[0].runner_name == "Ceddanne Rafaela"
    assert events[0].from_base == "1st"
    assert events[0].to_base == "2nd"
    assert events[0].outcome == "safe"

    assert events[1].event_type == "wild_pitch"
    assert events[1].runner_name == "Wilyer Abreu"
    assert events[1].from_base == "1st"
    assert events[1].to_base == "2nd"
    assert events[1].outcome == "advance"

    assert events[2].event_type == "wild_pitch"
    assert events[2].runner_name == "Josh Lowe"
    assert events[2].from_base == "1st"
    assert events[2].to_base == "2nd"
    assert events[2].outcome == "advance"
