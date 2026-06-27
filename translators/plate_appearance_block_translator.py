from __future__ import annotations

from models.plate_appearance_block import PlateAppearanceBlock


def translate_pa_block(pa_block: str) -> PlateAppearanceBlock:
    lines = [
        line.strip()
        for line in pa_block.splitlines()
        if line.strip()
    ]

    if not lines:
        return PlateAppearanceBlock(action_text="")

    return PlateAppearanceBlock(
        action_text=lines[-1],
        pitch_lines=lines[:-1],
        raw_lines=lines,
    )


__all__ = [
    "translate_pa_block",
]