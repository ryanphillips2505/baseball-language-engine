from __future__ import annotations

from assemblers.plate_appearance_builder import build_plate_appearance
from assemblers.timeline_block_builder import build_timeline_blocks
from models.game import Game
from models.plate_appearance_block import PlateAppearanceBlock


def build_game(
    pa_blocks: list[str] | list[PlateAppearanceBlock],
) -> Game:

    plate_appearances = []

    for block in pa_blocks:

        if isinstance(block, PlateAppearanceBlock):
            text = "\n".join(
                [
                    *block.pitch_lines,
                    block.action_text,
                ]
            )
        else:
            text = block

        plate_appearances.append(
            build_plate_appearance(text)
        )

    game = Game(
        plate_appearances=plate_appearances,
    )

    game.timeline.extend(
        build_timeline_blocks(pa_blocks)
    )

    return game


__all__ = [
    "build_game",
]
