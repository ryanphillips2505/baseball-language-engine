from __future__ import annotations

from typing import Any

from models.pitch_event import PitchEvent


_SWING_RESULTS = {
    "swinging strike",
    "swinging strike (blocked)",
    "foul",
    "foul tip",
    "foul bunt",
    "in play, out(s)",
    "in play, no out",
    "in play, run(s)",
}

_NO_SWING_RESULTS = {
    "ball",
    "ball in dirt",
    "called strike",
    "hit by pitch",
    "automatic ball",
    "automatic strike",
}


def _count_key(count: dict[str, Any] | None) -> str | None:
    if not isinstance(count, dict):
        return None
    balls = count.get("balls")
    strikes = count.get("strikes")
    if balls is None or strikes is None:
        return None
    return f"{balls}-{strikes}"


def _call_description(details: dict[str, Any]) -> str | None:
    call = details.get("call")
    if isinstance(call, dict):
        description = call.get("description")
        if isinstance(description, str) and description.strip():
            return description.strip()
    description = details.get("description")
    if isinstance(description, str) and description.strip():
        return description.strip()
    return None


def _pitch_type(details: dict[str, Any]) -> str | None:
    pitch_type = details.get("type")
    if isinstance(pitch_type, dict):
        description = pitch_type.get("description")
        if isinstance(description, str) and description.strip():
            return description.strip()
    return None


def _swing_flag(result: str, details: dict[str, Any]) -> bool | None:
    lowered = result.lower()
    if lowered in _SWING_RESULTS or details.get("isInPlay") is True:
        return True
    if lowered in _NO_SWING_RESULTS:
        return False
    if details.get("isStrike") is True and "swinging" in lowered:
        return True
    if details.get("isBall") is True:
        return False
    return None


def extract_mlb_statsapi_pitches(play: dict[str, Any]) -> list[PitchEvent]:
    """
    Extract pitch-level events from one StatsAPI allPlays entry.

    Only uses fields present on isPitch playEvents. Does not invent pitch data.
    """

    if not isinstance(play, dict):
        return []

    matchup = play.get("matchup") or {}
    batter_name = ((matchup.get("batter") or {}).get("fullName"))
    pitcher_name = ((matchup.get("pitcher") or {}).get("fullName"))

    pitches: list[PitchEvent] = []
    previous_count_after = "0-0"

    pitch_events = [
        event
        for event in play.get("playEvents") or []
        if isinstance(event, dict) and event.get("isPitch")
    ]

    for index, event in enumerate(pitch_events):
        details = event.get("details") or {}
        if not isinstance(details, dict):
            details = {}

        result = _call_description(details)
        if result is None:
            continue

        count_after = _count_key(event.get("count"))
        count_before = previous_count_after
        previous_count_after = count_after or previous_count_after

        pitch_data = event.get("pitchData") or {}
        velocity = None
        if isinstance(pitch_data, dict):
            start_speed = pitch_data.get("startSpeed")
            if isinstance(start_speed, (int, float)):
                velocity = float(start_speed)

        pitch_number = event.get("pitchNumber")
        if not isinstance(pitch_number, int):
            pitch_number = index + 1

        pitches.append(
            PitchEvent(
                pitch_number=pitch_number,
                count_before=count_before,
                result=result,
                swing=_swing_flag(result, details),
                ball_in_play=bool(details.get("isInPlay")),
                terminal_pitch=False,
                pitch_type=_pitch_type(details),
                velocity_mph=velocity,
                count_after=count_after,
                pitcher_name=pitcher_name if isinstance(pitcher_name, str) else None,
                batter_name=batter_name if isinstance(batter_name, str) else None,
            )
        )

    if pitches:
        pitches[-1].terminal_pitch = True

    return pitches


__all__ = [
    "extract_mlb_statsapi_pitches",
]
