from __future__ import annotations

from collections.abc import Callable

from models.timeline_block import TimelineBlock

CleanedPlateAppearanceBlocks = list[str]
CleanedTimelineBlocks = list[TimelineBlock]

Cleaner = Callable[[str], CleanedPlateAppearanceBlocks]
TimelineCleaner = Callable[[str], CleanedTimelineBlocks]

__all__ = [
    "CleanedPlateAppearanceBlocks",
    "CleanedTimelineBlocks",
    "Cleaner",
    "TimelineCleaner",
]
