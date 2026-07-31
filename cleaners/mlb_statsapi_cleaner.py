from __future__ import annotations

import json
from typing import Any

from cleaners.mlb_timeline_cleaner import timeline_blocks_from_mlb_play_lines
from models.timeline_block import TimelineBlock


def looks_like_mlb_statsapi_live_feed(raw_text: str) -> bool:
    """
    Detect a StatsAPI live feed JSON document.

    This is intentionally MLB-specific and does not classify other sources.
    """

    text = raw_text.lstrip()
    if not text.startswith("{"):
        return False

    try:
        payload = json.loads(raw_text)
    except json.JSONDecodeError:
        return False

    if not isinstance(payload, dict):
        return False

    live_data = payload.get("liveData")
    if not isinstance(live_data, dict):
        return False

    plays = live_data.get("plays")
    if not isinstance(plays, dict):
        return False

    all_plays = plays.get("allPlays")
    if not isinstance(all_plays, list):
        return False

    game_data = payload.get("gameData")
    if not isinstance(game_data, dict):
        return False

    # StatsAPI live feeds include copyright and/or gamePk metadata.
    copyright = str(payload.get("copyright") or "")
    has_mlb_marker = (
        "mlb" in copyright.lower()
        or "gamePk" in game_data
        or isinstance(payload.get("gamePk"), int)
    )

    return has_mlb_marker and len(all_plays) >= 0


def _load_statsapi_live_feed(raw_text: str) -> dict[str, Any]:
    if not looks_like_mlb_statsapi_live_feed(raw_text):
        raise ValueError("Input is not an MLB StatsAPI live feed JSON document")

    return json.loads(raw_text)


def extract_mlb_statsapi_play_descriptions(raw_text: str) -> list[str]:
    """
    Extract ordered allPlays result descriptions from a StatsAPI live feed.

    Preserves official MLB wording. Does not invent plays.
    """

    payload = _load_statsapi_live_feed(raw_text)
    all_plays = payload["liveData"]["plays"]["allPlays"]

    descriptions: list[str] = []
    for play in all_plays:
        if not isinstance(play, dict):
            continue
        result = play.get("result") or {}
        description = result.get("description")
        if isinstance(description, str) and description.strip():
            descriptions.append(description.strip())

    return descriptions


def clean_mlb_statsapi_text(raw_text: str) -> list[str]:
    """
    MLB-specific cleaner for StatsAPI live feed JSON.

    Returns one cleaned play line per allPlays description.
    """

    return extract_mlb_statsapi_play_descriptions(raw_text)


def clean_mlb_statsapi_timeline_text(raw_text: str) -> list[TimelineBlock]:
    """
    Convert StatsAPI live feed JSON into MLB timeline blocks.

    StatsAPI descriptions are already official play language, so they are not
    re-filtered through the Gameday page cleaner.
    """

    play_lines = clean_mlb_statsapi_text(raw_text)
    return timeline_blocks_from_mlb_play_lines(play_lines)


__all__ = [
    "looks_like_mlb_statsapi_live_feed",
    "extract_mlb_statsapi_play_descriptions",
    "clean_mlb_statsapi_text",
    "clean_mlb_statsapi_timeline_text",
]
