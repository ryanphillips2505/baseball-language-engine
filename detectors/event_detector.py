from __future__ import annotations

from models.detected_event import DetectedEvent
from models.types import EventType


def detect_event_types(pa_block: str) -> list[DetectedEvent]:
    """
    Detect event types present in a plate appearance block.

    This is detection only.

    No player extraction.
    No stat calculation.
    No normalization.
    No BaseballEvent creation.
    """

    text = pa_block.lower()

    events: list[DetectedEvent] = []

    #
    # HITS
    #

    if "singles" in text:
        events.append(DetectedEvent(event_type=EventType.SINGLE))

    if "doubles" in text:
        events.append(DetectedEvent(event_type=EventType.DOUBLE))

    if "ground-rule double" in text:
        events.append(DetectedEvent(event_type=EventType.DOUBLE))

    if "triples" in text:
        events.append(DetectedEvent(event_type=EventType.TRIPLE))

    if "homers" in text or "inside the park home run" in text:
        events.append(DetectedEvent(event_type=EventType.HOME_RUN))

    # iScore variants
    if "for a single" in text:
        events.append(DetectedEvent(event_type=EventType.SINGLE))

    if "for a double" in text:
        events.append(DetectedEvent(event_type=EventType.DOUBLE))

    if "for a triple" in text:
        events.append(DetectedEvent(event_type=EventType.TRIPLE))

    if "homerun" in text:
        events.append(DetectedEvent(event_type=EventType.HOME_RUN))
    
    if "singled" in text:
        events.append(DetectedEvent(event_type=EventType.SINGLE))

    if "doubled" in text and "doubled off" not in text:
        events.append(DetectedEvent(event_type=EventType.DOUBLE))

    if "tripled" in text:
        events.append(DetectedEvent(event_type=EventType.TRIPLE))

    if "homered" in text:
        events.append(DetectedEvent(event_type=EventType.HOME_RUN))
    
    if "infield single" in text:
        events.append(DetectedEvent(event_type=EventType.SINGLE))
    #
    # OUTS
    #

    if "grounds out" in text:
        events.append(DetectedEvent(event_type=EventType.GROUND_OUT))

    if "bunts out" in text:
        events.append(DetectedEvent(event_type=EventType.GROUND_OUT))

    if "bunts for an out" in text:
        events.append(DetectedEvent(event_type=EventType.GROUND_OUT))

    if "flies out" in text:
        events.append(DetectedEvent(event_type=EventType.FLY_OUT))

    if "lines out" in text:
        events.append(DetectedEvent(event_type=EventType.LINE_OUT))

    if "pops out" in text or "pops into" in text:
        events.append(DetectedEvent(event_type=EventType.POP_OUT))

    if " infield fly " in text:
        events.append(DetectedEvent(event_type=EventType.INFIELD_FLY))
    
    if "hits a line drive to the" in text and "for an out" in text:
        events.append(DetectedEvent(event_type=EventType.LINE_OUT))

    if "grounded out" in text:
        events.append(DetectedEvent(event_type=EventType.GROUND_OUT))

    if "grounded into" in text and "double play" not in text:
        events.append(DetectedEvent(event_type=EventType.GROUND_OUT))

    if "flied out" in text:
        events.append(DetectedEvent(event_type=EventType.FLY_OUT))

    if "lined out" in text:
        events.append(DetectedEvent(event_type=EventType.LINE_OUT))

    if "popped out" in text or "fouled out" in text:
        events.append(DetectedEvent(event_type=EventType.POP_OUT))

    #
    # STRIKEOUTS
    #

    if "strikes out looking" in text:
        events.append(DetectedEvent(event_type=EventType.STRIKEOUT_LOOKING))

    if "strikes out swinging" in text:
        events.append(DetectedEvent(event_type=EventType.STRIKEOUT_SWINGING))

    if "reaches on dropped 3rd strike" in text:
        events.append(DetectedEvent(event_type=EventType.DROPPED_THIRD_STRIKE_REACH))

    if "out at first on dropped 3rd strike" in text:
        events.append(DetectedEvent(event_type=EventType.STRIKEOUT_SWINGING))
    
    # Strikeout swinging variant
    if "strikes out on a foul tip" in text or "is out on foul tip" in text:
        events.append(DetectedEvent(event_type=EventType.STRIKEOUT_SWINGING))

    # Strikeout looking variant
    if "called out on strikes" in text:
        events.append(DetectedEvent(event_type=EventType.STRIKEOUT_LOOKING))

    if "strikes out but the third strike is dropped" in text and "thrown out" in text:
        events.append(
            DetectedEvent(event_type=EventType.DROPPED_THIRD_STRIKE_OUT)
        )
    
    if "struck out bunting foul" in text:
        events.append(
            DetectedEvent(
                event_type=EventType.STRIKEOUT_SWINGING
            )
        )

    if "struck out looking" in text:
        events.append(DetectedEvent(event_type=EventType.STRIKEOUT_LOOKING))

    if "struck out swinging" in text:
        events.append(DetectedEvent(event_type=EventType.STRIKEOUT_SWINGING))

    #
    # REACH EVENTS
    #

    # Intentional walks must win over generic walk wording (" walked").
    if "intentionally walk" in text:
        events.append(DetectedEvent(event_type=EventType.INTENTIONAL_WALK))
    else:
        if " walks" in text:
            events.append(DetectedEvent(event_type=EventType.WALK))

        if " is walked" in text:
            events.append(DetectedEvent(event_type=EventType.WALK))

        if " walked" in text:
            events.append(DetectedEvent(event_type=EventType.WALK))

    if " hit by pitch" in text:
        events.append(DetectedEvent(event_type=EventType.HIT_BY_PITCH))

    if "reaches on an error" in text:
        events.append(DetectedEvent(event_type=EventType.ERROR))

    if "reaches on a fielding error" in text:
        events.append(DetectedEvent(event_type=EventType.ERROR))

    if "reaches on a throwing error" in text:
        events.append(DetectedEvent(event_type=EventType.ERROR))

    if "reaches on a missed catch error" in text:
        events.append(DetectedEvent(event_type=EventType.ERROR))

    if " is hit by the pitch" in text:
        events.append(DetectedEvent(event_type=EventType.HIT_BY_PITCH))

    if "reaches base due to an error" in text:
        events.append(DetectedEvent(event_type=EventType.ERROR))
    
    #
    # SPECIAL EVENTS
    #

    if "sacrifice fly" in text:
        events.append(DetectedEvent(event_type=EventType.SAC_FLY))

    if "sacrifices" in text or "sacrifice bunt" in text:
        events.append(DetectedEvent(event_type=EventType.SAC_BUNT))

    if "fielder's choice double play" in text:
        events.append(DetectedEvent(event_type=EventType.FC_DOUBLE_PLAY))

    elif "grounds into a force out" in text:
        events.append(DetectedEvent(event_type=EventType.FIELDERS_CHOICE))

    elif "fielder's choice" in text:
        events.append(DetectedEvent(event_type=EventType.FIELDERS_CHOICE))

    elif "double play" in text:
        events.append(DetectedEvent(event_type=EventType.DOUBLE_PLAY))
    if "bunts to reach first safely" in text:
        events.append(DetectedEvent(event_type=EventType.SINGLE))

    if "is forced out at second" in text:
        events.append(DetectedEvent(event_type=EventType.FIELDERS_CHOICE))
        
        
    #
    # BASERUNNING EVENTS
    #

    if " steals " in f" {text} ":
        events.append(DetectedEvent(event_type=EventType.STOLEN_BASE))

    if " caught stealing " in f" {text} ":
        events.append(DetectedEvent(event_type=EventType.CAUGHT_STEALING))

    if " picked off " in f" {text} " or " picks off " in f" {text} ":
        events.append(DetectedEvent(event_type=EventType.PICKOFF))

    if " out advancing to " in text:
        events.append(DetectedEvent(event_type=EventType.RUNNER_OUT))

    if " wild pitch" in text:
        events.append(DetectedEvent(event_type=EventType.WILD_PITCH_ADVANCE))

    if " passed ball" in text:
        events.append(DetectedEvent(event_type=EventType.PASSED_BALL_ADVANCE))

    if " stole " in f" {text} ":
        events.append(DetectedEvent(event_type=EventType.STOLEN_BASE))

    for event in events:
        if event.event_type not in {
            EventType.STOLEN_BASE,
            EventType.CAUGHT_STEALING,
            EventType.PICKOFF,
            EventType.RUNNER_OUT,
            EventType.WILD_PITCH_ADVANCE,
            EventType.PASSED_BALL_ADVANCE,
        }:
            event.make_primary()
            break

    # Attach secondary error language after primary selection so hits / FC
    # remain primary when a fielding/throwing error is also mentioned.
    if (
        "fielding error by" in text
        or "throwing error by" in text
        or "missed catch error by" in text
        or " on a throwing error" in text
        or " on a fielding error" in text
    ):
        if not any(event.event_type == EventType.ERROR for event in events):
            events.append(
                DetectedEvent(event_type=EventType.ERROR, is_primary=False)
            )

    return events

