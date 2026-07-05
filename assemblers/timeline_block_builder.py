from __future__ import annotations

from models.plate_appearance_block import PlateAppearanceBlock
from models.timeline_block import (
    GameEventBlock,
    PlateAppearanceBlock as TimelinePlateAppearanceBlock,
    TimelineBlock,
)


def build_timeline_blocks(
    pa_blocks: list[str] | list[PlateAppearanceBlock] | list[TimelineBlock],
) -> list[TimelineBlock]:

    timeline: list[TimelineBlock] = []

    for block in pa_blocks:

        if isinstance(block, TimelineBlock):
            timeline.append(block)
            continue

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
