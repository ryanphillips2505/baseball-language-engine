from __future__ import annotations

from assemblers.pitch_decision_builder import build_pitch_decisions
from classifiers.ball_type_classifier import classify_ball_type
from classifiers.bip_classifier import is_ball_in_play
from classifiers.location_classifier import classify_location
from detectors.event_detector import detect_event_types
from extractors.pitch_token_extractor import extract_pitch_tokens
from extractors.player_extractor import extract_batter_name
from extractors.runner_event_extractor import extract_runner_events
from models.plate_appearance import PlateAppearance
from translators.base_translator import detected_events_to_baseball_event


def _extract_action_text(pa_block: str) -> str:
    lines = [
        line.strip()
        for line in str(pa_block or "").splitlines()
        if line.strip()
    ]

    if not lines:
        return ""

    return lines[-1]


def build_plate_appearance(pa_block: str) -> PlateAppearance:
    action_text = _extract_action_text(pa_block)

    detected_events = detect_event_types(action_text)

    baseball_event = detected_events_to_baseball_event(
        detected_events
    )

    batter_name = extract_batter_name(action_text)

    location = classify_location(action_text)

    ball_type = classify_ball_type(action_text)

    is_bip = is_ball_in_play(baseball_event)

    runner_events = extract_runner_events(action_text)

    pitch_tokens = extract_pitch_tokens(
        str(pa_block or "").splitlines()
    )

    pitches = build_pitch_decisions(pitch_tokens)

    return PlateAppearance(
        batter_name=batter_name,
        baseball_event=baseball_event,
        pitches=pitches,
        runner_events=runner_events,
        ball_type=ball_type,
        location=location,
        is_bip=is_bip,
    )


__all__ = [
    "build_plate_appearance",
]