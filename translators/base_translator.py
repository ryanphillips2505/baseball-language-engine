from __future__ import annotations

from models.baseball_event import BaseballEvent
from models.detected_event import DetectedEvent


def detected_events_to_baseball_event(
    detected_events: list[DetectedEvent],
) -> BaseballEvent | None:
    primary_events = [event for event in detected_events if event.is_primary]

    if not primary_events:
        return None

    primary_event = primary_events[0]

    secondary_events = [
        event.event_type
        for event in detected_events
        if not event.is_primary
    ]

    return BaseballEvent(
        primary_event=primary_event.event_type,
        secondary_events=secondary_events,
    )
