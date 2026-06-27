from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class PlateAppearanceBlock:
    """
    Source-independent intermediate representation of one plate appearance.

    This is the contract between the cleaning stage and the game-building stage.
    Every provider should eventually normalize its play-by-play into this object.
    """

    action_text: str

    pitch_lines: list[str] = field(default_factory=list)

    raw_lines: list[str] = field(default_factory=list)


__all__ = [
    "PlateAppearanceBlock",
]