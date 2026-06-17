from __future__ import annotations

import re

from models.runner_event import RunnerEvent


_RUNNER_NAME_RE = r"[A-Z][A-Za-z'.-]*(?:\s+[A-Z][A-Za-z'.-]*)*"


def _extract_runner_name(pa_block: str) -> str | None:
    """
    Extract runner name from common stolen-base phrases.

    Supports:

    John Smith steals second base.
    J. Walk stole third.
    M. Jones caught stealing second.

    And embedded GameChanger pitch sequences:

    Strike 1 swinging, Z Khalil steals 2nd, Foul.
    Ball 1, Preston Klose caught stealing 2nd, shortstop Ethan Vinson.
    """

    patterns = [
        rf"({_RUNNER_NAME_RE})\s+steals\s+(second|2nd|2b)",
        rf"({_RUNNER_NAME_RE})\s+stole\s+(second|2nd|2b)",
        rf"({_RUNNER_NAME_RE})\s+steals\s+(third|3rd|3b)",
        rf"({_RUNNER_NAME_RE})\s+stole\s+(third|3rd|3b)",
        rf"({_RUNNER_NAME_RE})\s+caught stealing\s+(second|2nd|2b)",
        rf"({_RUNNER_NAME_RE})\s+caught stealing\s+(third|3rd|3b)",
    ]

    for pattern in patterns:
        match = re.search(pattern, pa_block, re.IGNORECASE)

        if match:
            return match.group(1).strip()

    return None


def extract_runner_events(pa_block: str) -> list[RunnerEvent]:
    """
    Extract runner events from a plate appearance block.
    """

    text = pa_block.lower()
    events: list[RunnerEvent] = []

    runner_name = _extract_runner_name(pa_block)

    #
    # CAUGHT STEALING
    #

    if re.search(r"\bcaught stealing (second|2nd|2b)\b", text):
        events.append(
            RunnerEvent(
                event_type="CS",
                base="2B",
                runner_name=runner_name,
            )
        )

    if re.search(r"\bcaught stealing (third|3rd|3b)\b", text):
        events.append(
            RunnerEvent(
                event_type="CS",
                base="3B",
                runner_name=runner_name,
            )
        )

    #
    # STOLEN BASES
    #

    if re.search(r"\b(steals|stole|steal) (second|2nd|2b)\b", text):
        events.append(
            RunnerEvent(
                event_type="SB",
                base="2B",
                runner_name=runner_name,
            )
        )

    if re.search(r"\b(steals|stole|steal) (third|3rd|3b)\b", text):
        events.append(
            RunnerEvent(
                event_type="SB",
                base="3B",
                runner_name=runner_name,
            )
        )

    if re.search(r"\badvances to (second|2nd|2b) on stolen base\b", text):
        events.append(
            RunnerEvent(
                event_type="SB",
                base="2B",
                runner_name=runner_name,
            )
        )

    if re.search(r"\badvances to (third|3rd|3b) on stolen base\b", text):
        events.append(
            RunnerEvent(
                event_type="SB",
                base="3B",
                runner_name=runner_name,
            )
        )

    return events