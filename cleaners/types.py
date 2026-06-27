from __future__ import annotations

from collections.abc import Callable


CleanedPlateAppearanceBlocks = list[str]

Cleaner = Callable[[str], CleanedPlateAppearanceBlocks]


__all__ = [
    "CleanedPlateAppearanceBlocks",
    "Cleaner",
]