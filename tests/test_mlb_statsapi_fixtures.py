from __future__ import annotations

import json
from pathlib import Path

from cleaners.mlb_statsapi_cleaner import (
    clean_mlb_statsapi_text,
    looks_like_mlb_statsapi_live_feed,
)
from detectors.event_detector import detect_event_types
from detectors.source_detector import SourceType, detect_source
from models.types import EventType
from pipeline.process_game import process_game
from translators.base_translator import detected_events_to_baseball_event


STATSAPI_RAW = Path("samples/mlb/statsapi/raw")
STATSAPI_EXPECTED = Path("samples/mlb/statsapi/expected")

FIXTURES = [
    "mlb_angels_athletics_2026_06_20_gamepk824988",
    "mlb_redsox_mariners_2026_06_20_gamepk823126",
    "mlb_redsox_angels_2026_07_04_gamepk824012",
]


def _raw_path(stem: str) -> Path:
    return STATSAPI_RAW / f"{stem}.live.json"


def _expected_path(stem: str) -> Path:
    return STATSAPI_EXPECTED / f"{stem}.expected.json"


def test_mlb_statsapi_raw_and_expected_fixtures_exist():
    assert (STATSAPI_RAW / "manifest.json").exists()

    for stem in FIXTURES:
        assert _raw_path(stem).exists(), stem
        assert _expected_path(stem).exists(), stem


def test_mlb_statsapi_live_feed_is_detected_as_mlb():
    for stem in FIXTURES:
        raw = _raw_path(stem).read_text(encoding="utf-8")
        assert looks_like_mlb_statsapi_live_feed(raw)
        assert detect_source(raw) == SourceType.MLB


def test_mlb_statsapi_detection_does_not_claim_gamechanger_or_iscore():
    gc = Path("samples/gamechanger/raw/gamechanger_pa_blocks.txt").read_text(
        encoding="utf-8"
    )
    iscore = Path("samples/iscore/raw/iscore_raw_game_01.txt").read_text(
        encoding="utf-8"
    )

    assert looks_like_mlb_statsapi_live_feed(gc) is False
    assert looks_like_mlb_statsapi_live_feed(iscore) is False
    assert detect_source(gc) == SourceType.GAMECHANGER
    assert detect_source(iscore) == SourceType.ISCORE


def test_mlb_statsapi_cleaner_preserves_every_allplays_description():
    for stem in FIXTURES:
        raw = _raw_path(stem).read_text(encoding="utf-8")
        expected = json.loads(_expected_path(stem).read_text(encoding="utf-8"))

        cleaned = clean_mlb_statsapi_text(raw)

        assert cleaned == expected["all_play_descriptions"]
        assert len(cleaned) == expected["all_plays_count"]


def test_mlb_statsapi_cleaner_does_not_emit_json_chrome():
    raw = _raw_path(FIXTURES[0]).read_text(encoding="utf-8")
    cleaned = clean_mlb_statsapi_text(raw)

    for line in cleaned:
        assert not line.strip().startswith('"')
        assert '"description"' not in line
        assert line != "Hit By Pitch"
        assert line != "Walk"
        assert line != "Strikeout"


def test_mlb_statsapi_every_play_description_detects_an_event():
    undetected: list[tuple[str, str]] = []

    for stem in FIXTURES:
        raw = _raw_path(stem).read_text(encoding="utf-8")
        for description in clean_mlb_statsapi_text(raw):
            detected = detect_event_types(description)
            event = detected_events_to_baseball_event(detected)
            if event is None:
                undetected.append((stem, description))

    assert undetected == [], (
        "StatsAPI descriptions with no detected event:\n"
        + "\n".join(f"{stem}: {desc}" for stem, desc in undetected)
    )


def test_mlb_statsapi_angels_athletics_known_play_results():
    raw = _raw_path(
        "mlb_angels_athletics_2026_06_20_gamepk824988"
    ).read_text(encoding="utf-8")
    game = process_game(raw)

    by_desc = {
        pa.baseball_event.primary_event: True
        for pa in game.plate_appearances
        if pa.baseball_event is not None
    }

    assert EventType.WALK in by_desc
    assert EventType.SINGLE in by_desc
    assert EventType.DOUBLE in by_desc
    assert EventType.HOME_RUN in by_desc
    assert EventType.STRIKEOUT_SWINGING in by_desc
    assert EventType.STRIKEOUT_LOOKING in by_desc
    assert EventType.GROUND_OUT in by_desc
    assert EventType.FLY_OUT in by_desc


def test_mlb_statsapi_team_boxscore_strikeouts_and_walks_reconcile():
    """
    Reconcile parser-detected K/BB counts to StatsAPI team batting totals.

    Definitions used:
    - K = strikeout_looking + strikeout_swinging + dropped-third-strike outs
    - BB = walk + intentional_walk
    """

    for stem in FIXTURES:
        raw = _raw_path(stem).read_text(encoding="utf-8")
        expected = json.loads(_expected_path(stem).read_text(encoding="utf-8"))
        game = process_game(raw)

        k = 0
        bb = 0
        hr = 0
        doubles = 0
        triples = 0

        for pa in game.plate_appearances:
            if not pa.baseball_event:
                continue
            event = pa.baseball_event.primary_event
            if event in {
                EventType.STRIKEOUT_LOOKING,
                EventType.STRIKEOUT_SWINGING,
                EventType.DROPPED_THIRD_STRIKE_OUT,
            }:
                k += 1
            elif event in {EventType.WALK, EventType.INTENTIONAL_WALK}:
                bb += 1
            elif event == EventType.HOME_RUN:
                hr += 1
            elif event == EventType.DOUBLE:
                doubles += 1
            elif event == EventType.TRIPLE:
                triples += 1

        team = expected["team_batting"]
        expected_k = team["away"]["strikeOuts"] + team["home"]["strikeOuts"]
        expected_bb = team["away"]["baseOnBalls"] + team["home"]["baseOnBalls"]
        expected_hr = team["away"]["homeRuns"] + team["home"]["homeRuns"]
        expected_2b = team["away"]["doubles"] + team["home"]["doubles"]
        expected_3b = team["away"]["triples"] + team["home"]["triples"]

        assert k == expected_k, f"{stem}: K parser={k} box={expected_k}"
        assert bb == expected_bb, f"{stem}: BB parser={bb} box={expected_bb}"
        assert hr == expected_hr, f"{stem}: HR parser={hr} box={expected_hr}"
        assert doubles == expected_2b, (
            f"{stem}: 2B parser={doubles} box={expected_2b}"
        )
        assert triples == expected_3b, (
            f"{stem}: 3B parser={triples} box={expected_3b}"
        )
