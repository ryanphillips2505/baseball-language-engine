from __future__ import annotations

from models.types import EventType


def detect_event_types(pa_block: str) -> list[EventType]:
    """
    Detect event types present in a plate appearance block.

    This is detection only.

    No player extraction.
    No stat calculation.
    No normalization.
    No BaseballEvent creation.
    """

    text = pa_block.lower()

    events: list[EventType] = []

    #
    # HITS
    #

    if " singles " in f" {text} ":
        events.append(EventType.SINGLE)

    if " doubles " in f" {text} ":
        events.append(EventType.DOUBLE)

    if " triples " in f" {text} ":
        events.append(EventType.TRIPLE)

    if " homers " in f" {text} ":
        events.append(EventType.HOME_RUN)

    #
    # OUTS
    #

    if " grounds out " in f" {text} ":
        events.append(EventType.GROUND_OUT)

    if " flies out " in f" {text} ":
        events.append(EventType.FLY_OUT)

    if " lines out " in f" {text} ":
        events.append(EventType.LINE_OUT)

    if " pops out " in f" {text} ":
        events.append(EventType.POP_OUT)

    if " infield fly " in text:
        events.append(EventType.INFIELD_FLY)

    #
    # STRIKEOUTS
    #
    
    if "strikes out looking" in text:
        events.append(EventType.STRIKEOUT_LOOKING)
    
    if "strikes out swinging" in text:
        events.append(EventType.STRIKEOUT_SWINGING)
    
    if "reaches on dropped 3rd strike" in text:
        events.append(EventType.DROPPED_THIRD_STRIKE_REACH)
    
    if "out at first on dropped 3rd strike" in text:
        events.append(EventType.DROPPED_THIRD_STRIKE_OUT)

    #
    # REACH EVENTS
    #

    if " walks" in text:
        events.append(EventType.WALK)

    if " hit by pitch" in text:
        events.append(EventType.HIT_BY_PITCH)

    if " reaches on an error " in f" {text} ":
        events.append(EventType.ERROR)

    return events
