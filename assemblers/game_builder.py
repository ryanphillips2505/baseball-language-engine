from __future__ import annotations

from assemblers.game_event_builder import build_game_event
from assemblers.plate_appearance_builder import build_plate_appearance
from assemblers.timeline_builder import build_timeline
from models.game import Game
from models.plate_appearance_block import PlateAppearanceBlock
from models.timeline_block import (
    GameEventBlock,
    PlateAppearanceBlock as TimelinePlateAppearanceBlock,
    TimelineBlock,
)


def _text_from_legacy_pa_block(block: PlateAppearanceBlock) -> str:
    return "\n".join(
        [
            *block.pitch_lines,
            block.action_text,
        ]
    )


def build_game(
    pa_blocks: list[str] | list[PlateAppearanceBlock] | list[TimelineBlock],
) -> Game:

    plate_appearances = []

    for block in pa_blocks:

        if isinstance(block, GameEventBlock):
            continue

        if isinstance(block, TimelinePlateAppearanceBlock):
            text = block.raw_text

        elif isinstance(block, PlateAppearanceBlock):
            text = _text_from_legacy_pa_block(block)

        else:
            text = block

        plate_appearances.append(
            build_plate_appearance(text)
        )

    game = Game(
        plate_appearances=plate_appearances,
    )

    game.timeline = build_timeline(
        pa_blocks
    )

    for block in game.timeline.blocks:
        if isinstance(block, GameEventBlock):
            game_event = build_game_event(block)
            block.metadata["game_event"] = game_event

    return game


__all__ = [
    "build_game",
]
