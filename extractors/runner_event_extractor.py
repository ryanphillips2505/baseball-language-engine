from __future__ import annotations

import re

from models.runner_event import RunnerEvent


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
        r"([^,]+?)\s+steals\s+(second|2nd|2b)",
        r"([^,]+?)\s+stole\s+(second|2nd|2b)",
        r"([^,]+?)\s+steals\s+(third|3rd|3b)",
        r"([^,]+?)\s+stole\s+(third|3rd|3b)",
        r"([^,]+?)\s+caught stealing\s+(second|2nd|2b)",
        r"([^,]+?)\s+caught stealing\s+(third|3rd|3b)",
    ]

    for pattern in patterns:
        match = re.search(pattern, pa_block, re.IGNORECASE)

        if match:
            name = match.group(1).strip()

            #
            # Embedded GC pitch sequences:
            #
            # Strike 1 swinging, Z Khalil steals 2nd, Foul
            # Ball 1, Preston Klose caught stealing 2nd, ...
            #
            if "," in name:
                name = name.split(",")[-1].strip()

            return name

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