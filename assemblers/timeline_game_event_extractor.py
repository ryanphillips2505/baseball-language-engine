from __future__ import annotations

from models.timeline_block import GameEventBlock


def extract_game_events(
    timeline_blocks,
) -> list[GameEventBlock]:

    return [
        block
        for block in timeline_blocks
        if isinstance(block, GameEventBlock)
    ]
