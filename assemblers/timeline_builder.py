from __future__ import annotations

from assemblers.timeline_block_builder import build_timeline_blocks
from models.timeline import Timeline
from models.plate_appearance_block import PlateAppearanceBlock


def build_timeline(
    pa_blocks: list[str] | list[PlateAppearanceBlock],
) -> Timeline:

    timeline = Timeline()
    timeline.extend(
        build_timeline_blocks(pa_blocks)
    )

    return timeline
