from __future__ import annotations

from assemblers.game_builder import build_game
from assemblers.plate_appearance_grouper import group_gamechanger_plate_appearances
from cleaners.gamechanger_cleaner import normalize_pbp
from models.game import Game


def build_gamechanger_swing_game(raw_text: str) -> Game:
    lines = normalize_pbp(raw_text)
    plate_appearance_blocks = group_gamechanger_plate_appearances(lines)

    return build_game(plate_appearance_blocks)


__all__ = [
    "build_gamechanger_swing_game",
]