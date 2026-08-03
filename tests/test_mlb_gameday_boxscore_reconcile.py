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
    "redsox_dodgers_2026_08_02",
]

HIT_EVENTS = {
    EventType.SINGLE,
    EventType.DOUBLE,
    EventType.TRIPLE,
    EventType.HOME_RUN,
}


def _counts(stem: str) -> dict[str, int]:
    raw = Path(f"samples/mlb/validation/{stem}.txt").read_text(encoding="utf-8")
    game = process_game(raw)
    blocks = clean_mlb_timeline_text(raw)

    counts = {
        "K": 0,
        "BB": 0,
        "IBB": 0,
        "H": 0,
        "HR": 0,
        "2B": 0,
        "3B": 0,
        "HBP": 0,
        "SAC_BUNT": 0,
        "SAC_FLY": 0,
        "SB": 0,
        "CS": 0,
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
        elif event == EventType.INTENTIONAL_WALK:
            counts["BB"] += 1
            counts["IBB"] += 1
        elif event == EventType.WALK:
            counts["BB"] += 1
        elif event in HIT_EVENTS:
            counts["H"] += 1
            if event == EventType.HOME_RUN:
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

    def _runner_count(event_type: str) -> int:
        return sum(
            1
            for block in blocks
            if isinstance(block, GameEventBlock)
            and block.event_type == event_type
            and not (block.metadata or {}).get("administrative")
        )

    counts["SB"] = _runner_count("stolen_base")
    counts["CS"] = _runner_count("caught_stealing")
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
        "IBB": total("intentionalWalks"),
        "H": total("hits"),
        "HR": total("homeRuns"),
        "2B": total("doubles"),
        "3B": total("triples"),
        "HBP": total("hitByPitch"),
        "SAC_BUNT": total("sacBunts"),
        "SAC_FLY": total("sacFlies"),
        "SB": total("stolenBases"),
        "CS": total("caughtStealing"),
    }


def test_gameday_validation_corpus_boxscore_reconciles():
    """
    Scoped claim: on the reconciled Gameday / IQ Capture fixtures listed above,
    BLE plate-appearance / runner totals match StatsAPI team batting box scores
    for K, BB(+IBB), IBB, H, HR, 2B, 3B, HBP, sac bunts, sac flies, SB, and CS.
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

    # 4 games × 12 keys
    assert matched_keys == 48
    assert total_keys == 48
