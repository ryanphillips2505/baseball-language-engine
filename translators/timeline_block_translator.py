from __future__ import annotations

from models.timeline_block import PlateAppearanceBlock, TimelineBlock


def translate_timeline_blocks(
    cleaned_blocks: list[str],
) -> list[TimelineBlock]:

    return [
        PlateAppearanceBlock(
            raw_text=block,
        )
        for block in cleaned_blocks
    ]


__all__ = [
    "translate_timeline_blocks",
]
