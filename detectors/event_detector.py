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

    if "singles" in text:
        events.append(EventType.SINGLE)

    if "doubles" in text:
        events.append(EventType.DOUBLE)

    if "triples" in text:
        events.append(EventType.TRIPLE)

    if "homers" in text:
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

    #
    # SPECIAL EVENTS
    #

    if "sacrifice fly" in text:
        events.append(EventType.SAC_FLY)

    if "sacrifices" in text or "sacrifice bunt" in text:
        events.append(EventType.SAC_BUNT)

    if "fielder's choice double play" in text:
        events.append(EventType.FC_DOUBLE_PLAY)

    elif "fielder's choice" in text:
        events.append(EventType.FIELDERS_CHOICE)

    elif "double play" in text:
        events.append(EventType.DOUBLE_PLAY)

    #
    # BASERUNNING EVENTS
    #

    if " steals " in f" {text} ":
        events.append(EventType.STOLEN_BASE)

    if " caught stealing " in f" {text} ":
        events.append(EventType.CAUGHT_STEALING)

    if " picked off " in f" {text} ":
        events.append(EventType.PICKOFF)

    if " out advancing to " in text:
        events.append(EventType.RUNNER_OUT)

    if " wild pitch" in text:
        events.append(EventType.WILD_PITCH_ADVANCE)

    if " passed ball" in text:
        events.append(EventType.PASSED_BALL_ADVANCE)

    return events
