from __future__ import annotations

from assemblers.game_builder import build_game
from cleaners.cleaner_router import clean_by_source
from cleaners.mlb_statsapi_cleaner import (
    clean_mlb_statsapi_timeline_text,
    looks_like_mlb_statsapi_live_feed,
)
from cleaners.mlb_timeline_cleaner import clean_mlb_timeline_text
from detectors.source_detector import SourceType, detect_source_with_language_fallbacks
from language.reader import build_multi_platform_plate_appearance, infer_statcrew_ball_types
from language.substitutions import extract_runner_entries
from models.game import Game


def process_game(raw_text: str, source: SourceType | None = None) -> Game:
    """
    source: pass when the caller already knows the platform (e.g. a college
    SCOUTBINDER export reading a Sidearm page); otherwise it is detected.
    """
    # StatsAPI JSON must use the MLB StatsAPI cleaner. Passing raw JSON through
    # the Gameday text cleaner retains JSON chrome as false play lines.
    if source is None and looks_like_mlb_statsapi_live_feed(raw_text):
        blocks = clean_mlb_statsapi_timeline_text(raw_text)
        return _mark_multi_platform(build_game(blocks), "mlb", raw_text)

    if source is None:
        source = detect_source_with_language_fallbacks(raw_text)

    if source == SourceType.MLB:
        blocks = clean_mlb_timeline_text(raw_text)
    else:
        blocks = clean_by_source(raw_text, source)

    # GameChanger keeps the legacy reader: its output is frozen to the
    # production Opponent IQ GameChanger reading.
    if source == SourceType.GAMECHANGER:
        return build_game(blocks)

    game = build_game(
        blocks,
        plate_appearance_builder=build_multi_platform_plate_appearance,
    )
    if source == SourceType.COLLEGE:
        infer_statcrew_ball_types(game)
    return _mark_multi_platform(game, source.value, raw_text)


def _mark_multi_platform(game: Game, source: str, raw_text: str) -> Game:
    """Tag a non-GameChanger game so the aggregator adds H/ROE/FC/PR/CR."""
    game.source = source
    game.runner_entries = extract_runner_entries(raw_text)
    return game


__all__ = [
    "process_game",
]
