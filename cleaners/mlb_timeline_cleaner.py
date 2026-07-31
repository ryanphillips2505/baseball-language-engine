from __future__ import annotations

import re

from cleaners.mlb_cleaner import clean_mlb_text
from models.timeline_block import GameEventBlock, PlateAppearanceBlock, TimelineBlock


_CAUGHT_STEALING_RE = re.compile(
    r"\bcaught stealing\b",
    re.I,
)

_STOLEN_BASE_RE = re.compile(
    r"\bsteals\b",
    re.I,
)

_WILD_PITCH_RE = re.compile(
    r"\bwild pitch\b",
    re.I,
)

_PICKED_OFF_RE = re.compile(
    r"\bpicked off\b",
    re.I,
)

_PASSED_BALL_RE = re.compile(
    r"\bpassed ball\b",
    re.I,
)

_BALK_RE = re.compile(
    r"\bbalk\b",
    re.I,
)

_DEFENSIVE_INDIFFERENCE_RE = re.compile(
    r"\bdefensive indifference\b",
    re.I,
)


def timeline_blocks_from_mlb_play_lines(
    play_lines: list[str],
) -> list[TimelineBlock]:
    """
    Classify already-cleaned MLB play lines into timeline blocks.

    Used by Gameday text cleaning and StatsAPI JSON extraction so runner-only
    events stay separated from plate appearances.
    """

    timeline_blocks: list[TimelineBlock] = []

    for block in play_lines:

        if _CAUGHT_STEALING_RE.search(block):
            timeline_blocks.append(
                GameEventBlock(
                    raw_text=block,
                    event_type="caught_stealing",
                    source="mlb",
                )
            )
            continue

        if _STOLEN_BASE_RE.search(block):
            timeline_blocks.append(
                GameEventBlock(
                    raw_text=block,
                    event_type="stolen_base",
                    source="mlb",
                )
            )
            continue

        if _WILD_PITCH_RE.search(block):
            timeline_blocks.append(
                GameEventBlock(
                    raw_text=block,
                    event_type="wild_pitch",
                    source="mlb",
                )
            )
            continue

        if _PICKED_OFF_RE.search(block):
            timeline_blocks.append(
                GameEventBlock(
                    raw_text=block,
                    event_type="pickoff",
                    source="mlb",
                )
            )
            continue

        if _PASSED_BALL_RE.search(block):
            timeline_blocks.append(
                GameEventBlock(
                    raw_text=block,
                    event_type="passed_ball",
                    source="mlb",
                )
            )
            continue

        if _BALK_RE.search(block):
            timeline_blocks.append(
                GameEventBlock(
                    raw_text=block,
                    event_type="balk",
                    source="mlb",
                )
            )
            continue

        if _DEFENSIVE_INDIFFERENCE_RE.search(block):
            timeline_blocks.append(
                GameEventBlock(
                    raw_text=block,
                    event_type="defensive_indifference",
                    source="mlb",
                )
            )
            continue

        timeline_blocks.append(
            PlateAppearanceBlock(
                raw_text=block,
                source="mlb",
            )
        )

    return timeline_blocks


def clean_mlb_timeline_text(raw_text: str) -> list[TimelineBlock]:
    cleaned = clean_mlb_text(raw_text)
    return timeline_blocks_from_mlb_play_lines(cleaned)


__all__ = [
    "clean_mlb_timeline_text",
    "timeline_blocks_from_mlb_play_lines",
]
