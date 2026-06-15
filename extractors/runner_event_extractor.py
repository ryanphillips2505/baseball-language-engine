from __future__ import annotations

import re

from models.runner_event import RunnerEvent


def extract_runner_events(pa_block: str) -> list[RunnerEvent]:
    """
    Extract simple runner events from a plate appearance block.

    Phase 6 scope:
    - Stolen base to second
    - Stolen base to third
    - Caught stealing second
    - Caught stealing third

    No runner identity extraction.
    No base-state tracking.
    No run scoring.
    """

    text = pa_block.lower()
    events: list[RunnerEvent] = []

    #
    # CAUGHT STEALING
    #

    if re.search(r"\bcaught stealing (second|2nd|2b)\b", text):
        events.append(RunnerEvent(event_type="CS", base="2B"))

    if re.search(r"\bcaught stealing (third|3rd|3b)\b", text):
        events.append(RunnerEvent(event_type="CS", base="3B"))

    #
    # STOLEN BASES
    #

    if re.search(r"\b(steals|stole|steal) (second|2nd|2b)\b", text):
        events.append(RunnerEvent(event_type="SB", base="2B"))

    if re.search(r"\b(steals|stole|steal) (third|3rd|3b)\b", text):
        events.append(RunnerEvent(event_type="SB", base="3B"))

    if re.search(r"\badvances to (second|2nd|2b) on stolen base\b", text):
        events.append(RunnerEvent(event_type="SB", base="2B"))

    if re.search(r"\badvances to (third|3rd|3b) on stolen base\b", text):
        events.append(RunnerEvent(event_type="SB", base="3B"))

    return events
