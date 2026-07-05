from __future__ import annotations

from assemblers.plate_appearance_builder import build_plate_appearance
from models.game import Game
from models.plate_appearance_block import PlateAppearanceBlock
from models.timeline_block import PlateAppearanceBlock as TimelinePlateAppearanceBlock


def build_game(
    pa_blocks: list[str] | list[PlateAppearanceBlock],
) -> Game:
    plate_appearances = []
    timeline_blocks = []

    for block in pa_blocks:
        if isinstance(block, PlateAppearanceBlock):
            text = "\n".join(
                [
                    *block.pitch_lines,
                    block.action_text,
                ]
            )

            timeline_blocks.append(
                TimelinePlateAppearanceBlock(
                    raw_text=text,
                )
            )

        else:
            text = block

            timeline_blocks.append(
                TimelinePlateAppearanceBlock(
                    raw_text=text,
                )
            )

        plate_appearances.append(
            build_plate_appearance(text)
        )

    game = Game(
        plate_appearances=plate_appearances,
    )

    game.timeline.extend(timeline_blocks)

    return game


__all__ = [
    "build_game",
]
