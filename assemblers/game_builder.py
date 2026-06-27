from __future__ import annotations

from assemblers.plate_appearance_builder import build_plate_appearance
from models.game import Game


def build_game(pa_blocks: list[str]) -> Game:
    plate_appearances = [
        build_plate_appearance(pa_block)
        for pa_block in pa_blocks
    ]

    return Game(plate_appearances=plate_appearances)


__all__ = [
    "build_game",
]
