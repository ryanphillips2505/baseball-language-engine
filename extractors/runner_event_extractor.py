from __future__ import annotations

import re

from models.runner_event import RunnerEvent


_RUNNER_NAME_RE = r"[A-Z][A-Za-z'.-]*(?:\s+[A-Z][A-Za-z'.-]*)*"
_STEAL_TOTAL_RE = r"(?:\(\d+\)\s+)?"


def _iter_runner_events(
    pa_block: str,
    pattern: str,
    event_type: str,
    base: str,
) -> list[RunnerEvent]:
    events: list[RunnerEvent] = []

    for match in re.finditer(pattern, pa_block, re.IGNORECASE):
        runner = match.groupdict().get("runner")

        events.append(
            RunnerEvent(
                event_type=event_type,
                base=base,
                runner_name=runner.strip() if runner else None,
            )
        )

    return events


def extract_runner_events(pa_block: str) -> list[RunnerEvent]:
    events: list[RunnerEvent] = []

    patterns = [
        (
            rf"(?P<runner>{_RUNNER_NAME_RE})\s+(?:steals|stole|steal)\s+{_STEAL_TOTAL_RE}(?:second|2nd|2b)\b",
            "SB",
            "2B",
        ),
        (
            rf"(?P<runner>{_RUNNER_NAME_RE})\s+(?:steals|stole|steal)\s+{_STEAL_TOTAL_RE}(?:third|3rd|3b)\b",
            "SB",
            "3B",
        ),
        (
            rf"(?:^|[,.]\s*)(?:steals|stole|steal)\s+{_STEAL_TOTAL_RE}(?:second|2nd|2b)\b",
            "SB",
            "2B",
        ),
        (
            rf"(?:^|[,.]\s*)(?:steals|stole|steal)\s+{_STEAL_TOTAL_RE}(?:third|3rd|3b)\b",
            "SB",
            "3B",
        ),
        (
            rf"(?P<runner>{_RUNNER_NAME_RE})\s+caught stealing\s+(?:second|2nd|2b)\b",
            "CS",
            "2B",
        ),
        (
            rf"(?P<runner>{_RUNNER_NAME_RE})\s+caught stealing\s+(?:third|3rd|3b)\b",
            "CS",
            "3B",
        ),
        (
            rf"(?P<runner>{_RUNNER_NAME_RE})\s+caught stealing\s+(?:home|home plate)\b",
            "CS",
            "HOME",
        ),
    ]

    for pattern, event_type, base in patterns:
        events.extend(
            _iter_runner_events(
                pa_block=pa_block,
                pattern=pattern,
                event_type=event_type,
                base=base,
            )
        )

    return events
