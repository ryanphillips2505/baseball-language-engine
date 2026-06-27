from __future__ import annotations

from cleaners.cleaner_router import clean_by_source
from assemblers.plate_appearance_builder import build_plate_appearance
from models.game import Game


def process_game(raw_text: str) -> Game:
    cleaned_plate_appearances = clean_by_source(raw_text)

    plate_appearances = [
        build_plate_appearance(pa_block)
        for pa_block in cleaned_plate_appearances
    ]

    return Game(plate_appearances=plate_appearances)


__all__ = [
    "process_game",
]