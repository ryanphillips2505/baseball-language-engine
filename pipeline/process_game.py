from __future__ import annotations

from assemblers.game_builder import build_game
from cleaners.cleaner_router import clean_by_source
from models.game import Game


def process_game(raw_text: str) -> Game:
    cleaned_plate_appearances = clean_by_source(raw_text)

    return build_game(cleaned_plate_appearances)


__all__ = [
    "process_game",
]