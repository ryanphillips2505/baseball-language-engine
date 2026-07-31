from __future__ import annotations

import json
from pathlib import Path

from cleaners.mlb_timeline_cleaner import clean_mlb_timeline_text
from models.timeline_block import GameEventBlock
from models.types import EventType
from pipeline.process_game import process_game


# Full-game Gameday pastes that reconcile to StatsAPI team batting box scores.
RECONCILED_FIXTURES = [
    "rangers_rays_2026_07_30",
    "marlins_mets_2026_07_30",
    "redsox_athletics_2026_07_30",
]


def _counts(stem: str) -> dict[str, int]:
    raw = Path(f"samples/mlb/validation/{stem}.txt").read_text(encoding="utf-8")
    game = process_game(raw)
    blocks = clean_mlb_timeline_text(raw)

    counts = {
        "K": 0,
        "BB": 0,
        "HR": 0,
        "2B": 0,
        "3B": 0,
        "HBP": 0,
        "SAC_BUNT": 0,
        "SAC_FLY": 0,
        "SB": 0,
    }

    for pa in game.plate_appearances:
        if not pa.baseball_event:
            continue
        event = pa.baseball_event.primary_event
        if event in {
            EventType.STRIKEOUT_LOOKING,
            EventType.STRIKEOUT_SWINGING,
            EventType.DROPPED_THIRD_STRIKE_OUT,
        }:
            counts["K"] += 1
        elif event in {EventType.WALK, EventType.INTENTIONAL_WALK}:
            counts["BB"] += 1
        elif event == EventType.HOME_RUN:
            counts["HR"] += 1
        elif event == EventType.DOUBLE:
            counts["2B"] += 1
        elif event == EventType.TRIPLE:
            counts["3B"] += 1
        elif event == EventType.HIT_BY_PITCH:
            counts["HBP"] += 1
        elif event == EventType.SAC_BUNT:
            counts["SAC_BUNT"] += 1
        elif event == EventType.SAC_FLY:
            counts["SAC_FLY"] += 1

    counts["SB"] = sum(
        1
        for block in blocks
        if isinstance(block, GameEventBlock)
        and block.event_type == "stolen_base"
        and not (block.metadata or {}).get("administrative")
    )
    return counts


def _box_totals(stem: str) -> dict[str, int]:
    expected = json.loads(
        Path(f"samples/mlb/validation/expected/{stem}.boxscore.json").read_text(
            encoding="utf-8"
        )
    )
    team = expected["team_batting"]

    def total(key: str) -> int:
        return int(team["away"][key]) + int(team["home"][key])

    return {
        "K": total("strikeOuts"),
        "BB": total("baseOnBalls"),
        "HR": total("homeRuns"),
        "2B": total("doubles"),
        "3B": total("triples"),
        "HBP": total("hitByPitch"),
        "SAC_BUNT": total("sacBunts"),
        "SAC_FLY": total("sacFlies"),
        "SB": total("stolenBases"),
    }


def test_gameday_validation_corpus_boxscore_reconciles():
    """
    Scoped claim: on the three fully pasted 2026-07-30 Gameday fixtures,
    BLE plate-appearance / runner totals match StatsAPI team batting box scores
    for K, BB(+IBB), HR, 2B, 3B, HBP, sac bunts, sac flies, and SB.
    """

    matched_keys = 0
    total_keys = 0

    for stem in RECONCILED_FIXTURES:
        got = _counts(stem)
        expected = _box_totals(stem)
        for key in expected:
            total_keys += 1
            assert got[key] == expected[key], (
                f"{stem}: {key} parser={got[key]} box={expected[key]}"
            )
            matched_keys += 1

    # 3 games × 9 keys
    assert matched_keys == 27
    assert total_keys == 27
