from __future__ import annotations

import json
from pathlib import Path

from extractors.mlb_statsapi_pitch_extractor import extract_mlb_statsapi_pitches
from models.pitch_event import PitchEvent
from pipeline.process_game import process_game


ANGELS_ATHLETICS = Path(
    "samples/mlb/statsapi/raw/mlb_angels_athletics_2026_06_20_gamepk824988.live.json"
)
RED_SOX_ANGELS_GAMEDAY = Path(
    "samples/mlb/validation/red_sox_angels_2026_07_04.txt"
)


def _feed() -> dict:
    return json.loads(ANGELS_ATHLETICS.read_text(encoding="utf-8"))


def _nolan_schanuel_challenge_strikeout(feed: dict) -> dict:
    for play in feed["liveData"]["plays"]["allPlays"]:
        description = (play.get("result") or {}).get("description") or ""
        if (
            "Nolan Schanuel called out on strikes" in description
            and "overturned" in description
        ):
            return play
    raise AssertionError("Expected Nolan Schanuel overturned called strikeout play")


def test_extract_mlb_statsapi_pitches_preserves_type_velocity_and_result():
    play = _nolan_schanuel_challenge_strikeout(_feed())
    pitches = extract_mlb_statsapi_pitches(play)

    assert len(pitches) == 4
    assert all(isinstance(pitch, PitchEvent) for pitch in pitches)

    assert pitches[0].pitch_number == 1
    assert pitches[0].count_before == "0-0"
    assert pitches[0].count_after == "0-1"
    assert pitches[0].result == "Foul"
    assert pitches[0].pitch_type == "Cutter"
    assert pitches[0].velocity_mph == 89.5
    assert pitches[0].swing is True
    assert pitches[0].ball_in_play is False
    assert pitches[0].batter_name == "Nolan Schanuel"
    assert pitches[0].pitcher_name == "J.T. Ginn"

    assert pitches[1].result == "Swinging Strike"
    assert pitches[1].pitch_type == "Changeup"
    assert pitches[1].velocity_mph == 88.0
    assert pitches[1].swing is True

    assert pitches[2].result == "Ball"
    assert pitches[2].swing is False
    assert pitches[2].count_before == "0-2"
    assert pitches[2].count_after == "1-2"

    assert pitches[3].result == "Called Strike"
    assert pitches[3].pitch_type == "Sinker"
    assert pitches[3].velocity_mph == 94.4
    assert pitches[3].swing is False
    assert pitches[3].terminal_pitch is True


def test_process_game_attaches_statsapi_pitches_to_plate_appearances():
    game = process_game(ANGELS_ATHLETICS.read_text(encoding="utf-8"))

    matching = [
        pa
        for pa in game.plate_appearances
        if pa.batter_name == "Nolan Schanuel"
        and pa.pitches
        and pa.pitches[-1].result == "Called Strike"
    ]
    assert matching
    assert matching[0].pitches[0].pitch_type == "Cutter"
    assert matching[0].pitches[0].velocity_mph == 89.5


def test_statsapi_fixture_pitch_totals_match_is_pitch_events():
    feed = _feed()
    expected_pitches = sum(
        1
        for play in feed["liveData"]["plays"]["allPlays"]
        for event in play.get("playEvents") or []
        if event.get("isPitch")
    )

    game = process_game(ANGELS_ATHLETICS.read_text(encoding="utf-8"))
    pa_pitches = sum(len(pa.pitches) for pa in game.plate_appearances)

    assert pa_pitches == expected_pitches
    assert len(game.pitch_events) == expected_pitches
    assert expected_pitches == 322


def test_statsapi_preserves_pitches_on_runner_only_plays():
    raw = Path(
        "samples/mlb/statsapi/raw/"
        "mlb_redsox_mariners_2026_06_20_gamepk823126.live.json"
    ).read_text(encoding="utf-8")
    feed = json.loads(raw)
    expected_pitches = sum(
        1
        for play in feed["liveData"]["plays"]["allPlays"]
        for event in play.get("playEvents") or []
        if event.get("isPitch")
    )

    game = process_game(raw)
    pa_pitches = sum(len(pa.pitches) for pa in game.plate_appearances)

    # Caught-stealing-home is a runner-only timeline event but still carries
    # the in-progress batter's pitch sequence in StatsAPI.
    assert pa_pitches < expected_pitches
    assert len(game.pitch_events) == expected_pitches
    assert expected_pitches == 279

    cs_pitches = [
        pitch
        for pitch in game.pitch_events
        if pitch.batter_name == "Carlos Narváez"
        and pitch.pitcher_name == "José A. Ferrer"
        and pitch.velocity_mph in {98.1, 99.2, 88.8, 98.8}
    ]
    assert len(cs_pitches) == 4


def test_gameday_text_path_does_not_invent_pitch_type_or_velocity():
    game = process_game(RED_SOX_ANGELS_GAMEDAY.read_text(encoding="utf-8"))

    assert game.pitch_events == []
    for pa in game.plate_appearances:
        for pitch in pa.pitches:
            if isinstance(pitch, PitchEvent):
                assert pitch.pitch_type is None
                assert pitch.velocity_mph is None
