from __future__ import annotations

from classifiers.location_classifier import classify_location
from detectors.event_detector import detect_event_types
from extractors.player_extractor import extract_batter_name
from models.plate_appearance import PlateAppearance
from translators.base_translator import detected_events_to_baseball_event


def build_plate_appearance(pa_block: str) -> PlateAppearance:
    detected_events = detect_event_types(pa_block)

    baseball_event = detected_events_to_baseball_event(
        detected_events
    )

    batter_name = extract_batter_name(pa_block)

    location = classify_location(pa_block)

    return PlateAppearance(
        batter_name=batter_name,
        baseball_event=baseball_event,
        pitches=[],
        location=location,
    )
