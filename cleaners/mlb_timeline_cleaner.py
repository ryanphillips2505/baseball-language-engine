from __future__ import annotations

import re

from cleaners.mlb_cleaner import clean_mlb_text
from models.timeline_block import GameEventBlock, PlateAppearanceBlock, TimelineBlock


_CAUGHT_STEALING_RE = re.compile(
    r"\bcaught stealing\b",
    re.I,
)

_STOLEN_BASE_RE = re.compile(
    r"\bsteals\b",
    re.I,
)


def clean_mlb_timeline_text(raw_text: str) -> list[TimelineBlock]:

    cleaned = clean_mlb_text(raw_text)

    timeline_blocks: list[TimelineBlock] = []

    for block in cleaned:

        if _CAUGHT_STEALING_RE.search(block):
            timeline_blocks.append(
                GameEventBlock(
                    raw_text=block,
                    event_type="caught_stealing",
                    source="mlb",
                )
            )
            continue

        if _STOLEN_BASE_RE.search(block):
            timeline_blocks.append(
                GameEventBlock(
                    raw_text=block,
                    event_type="stolen_base",
                    source="mlb",
                )
            )
            continue

        timeline_blocks.append(
            PlateAppearanceBlock(
                raw_text=block,
                source="mlb",
            )
        )

    return timeline_blocks


__all__ = [
    "clean_mlb_timeline_text",
]
