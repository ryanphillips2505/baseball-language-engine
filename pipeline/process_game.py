from __future__ import annotations

from assemblers.game_builder import build_game
from cleaners.cleaner_router import clean_by_source
from cleaners.mlb_statsapi_cleaner import (
    clean_mlb_statsapi_timeline_text,
    looks_like_mlb_statsapi_live_feed,
)
from cleaners.mlb_timeline_cleaner import clean_mlb_timeline_text
from detectors.source_detector import SourceType, detect_source
from models.game import Game


def process_game(raw_text: str) -> Game:
    # StatsAPI JSON must use the MLB StatsAPI cleaner. Passing raw JSON through
    # the Gameday text cleaner retains JSON chrome as false play lines.
    if looks_like_mlb_statsapi_live_feed(raw_text):
        blocks = clean_mlb_statsapi_timeline_text(raw_text)
        return build_game(blocks)

    source = detect_source(raw_text)

    if source == SourceType.MLB:
        blocks = clean_mlb_timeline_text(raw_text)
    else:
        blocks = clean_by_source(raw_text)

    return build_game(blocks)


__all__ = [
    "process_game",
]
