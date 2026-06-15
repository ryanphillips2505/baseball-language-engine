from classifiers.bip_classifier import is_ball_in_play
from models.baseball_event import BaseballEvent
from models.types import EventType


def make_event(event_type: EventType) -> BaseballEvent:
    return BaseballEvent(
        primary_event=event_type,
        secondary_events=[],
    )


def test_hit_events_are_bip():
    assert is_ball_in_play(make_event(EventType.SINGLE)) is True
    assert is_ball_in_play(make_event(EventType.DOUBLE)) is True
    assert is_ball_in_play(make_event(EventType.TRIPLE)) is True
    assert is_ball_in_play(make_event(EventType.HOME_RUN)) is True


def test_out_events_are_bip():
    assert is_ball_in_play(make_event(EventType.GROUND_OUT)) is True
    assert is_ball_in_play(make_event(EventType.FLY_OUT)) is True
    assert is_ball_in_play(make_event(EventType.LINE_OUT)) is True
    assert is_ball_in_play(make_event(EventType.POP_OUT)) is True


def test_non_bip_events_are_not_bip():
    assert is_ball_in_play(make_event(EventType.WALK)) is False
    assert is_ball_in_play(make_event(EventType.HIT_BY_PITCH)) is False
    assert is_ball_in_play(make_event(EventType.STRIKEOUT_SWINGING)) is False
    assert is_ball_in_play(make_event(EventType.STRIKEOUT_LOOKING)) is False


def test_none_is_not_bip():
    assert is_ball_in_play(None) is False