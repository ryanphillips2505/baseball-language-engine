from __future__ import annotations

from models.baseball_event import BaseballEvent
from models.types import EventType


BIP_EVENTS = {
    EventType.SINGLE,
    EventType.DOUBLE,
    EventType.TRIPLE,
    EventType.HOME_RUN,
    EventType.GROUND_OUT,
    EventType.FLY_OUT,
    EventType.LINE_OUT,
    EventType.POP_OUT,
    EventType.INFIELD_FLY,
    EventType.ERROR,
    EventType.FIELDERS_CHOICE,
    EventType.DOUBLE_PLAY,
    EventType.FC_DOUBLE_PLAY,
    EventType.SAC_BUNT,
    EventType.SAC_FLY,
}


def is_ball_in_play(baseball_event: BaseballEvent | None) -> bool:
    if baseball_event is None:
        return False

    return baseball_event.primary_event in BIP_EVENTS
