from __future__ import annotations

from models.plate_appearance_block import PlateAppearanceBlock
from models.timeline_block import (
    PlateAppearanceBlock as TimelinePlateAppearanceBlock,
)


def build_timeline_blocks(
    pa_blocks: list[str] | list[PlateAppearanceBlock],
) -> list[TimelinePlateAppearanceBlock]:

    timeline = []

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

        timeline.append(
            TimelinePlateAppearanceBlock(
                raw_text=text,
            )
        )

    return timeline
