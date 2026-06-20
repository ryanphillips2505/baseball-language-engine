from aggregators.swing_decision_aggregator import aggregate_swing_decisions
from models.baseball_event import BaseballEvent
from models.game import Game
from models.pitch_decision import PitchDecision, PitchOutcome
from models.plate_appearance import PlateAppearance
from models.types import EventType


def test_aggregates_swing_decisions_by_player_and_count():
    game = Game(
        plate_appearances=[
            PlateAppearance(
                batter_name="John Smith",
                baseball_event=BaseballEvent(
                    primary_event=EventType.SINGLE,
                    secondary_events=[],
                ),
                pitches=[
                    PitchDecision("0-0", PitchOutcome.BALL),
                    PitchDecision("1-0", PitchOutcome.CALLED_STRIKE),
                    PitchDecision("1-1", PitchOutcome.FOUL),
                    PitchDecision("1-2", PitchOutcome.BIP),
                ],
            )
        ]
    )

    stats = aggregate_swing_decisions(game)

    assert stats["John Smith"]["0-0"]["PA"] == 1
    assert stats["John Smith"]["0-0"]["BALL"] == 1
    assert stats["John Smith"]["1-0"]["CALLED_STRIKE"] == 1
    assert stats["John Smith"]["1-1"]["FOUL"] == 1
    assert stats["John Smith"]["1-2"]["BIP"] == 1


def test_foul_twice_at_same_count_counts_pa_once():
    game = Game(
        plate_appearances=[
            PlateAppearance(
                batter_name="John Smith",
                baseball_event=BaseballEvent(
                    primary_event=EventType.STRIKEOUT_SWINGING,
                    secondary_events=[],
                ),
                pitches=[
                    PitchDecision("0-0", PitchOutcome.CALLED_STRIKE),
                    PitchDecision("0-1", PitchOutcome.SWING_MISS),
                    PitchDecision("0-2", PitchOutcome.FOUL),
                    PitchDecision("0-2", PitchOutcome.FOUL),
                    PitchDecision("0-2", PitchOutcome.SWING_MISS),
                ],
            )
        ]
    )

    stats = aggregate_swing_decisions(game)

    assert stats["John Smith"]["0-2"]["PA"] == 1
    assert stats["John Smith"]["0-2"]["FOUL"] == 2
    assert stats["John Smith"]["0-2"]["SWING_MISS"] == 1


def test_aggregates_multiple_players():
    game = Game(
        plate_appearances=[
            PlateAppearance(
                batter_name="John Smith",
                baseball_event=BaseballEvent(
                    primary_event=EventType.WALK,
                    secondary_events=[],
                ),
                pitches=[
                    PitchDecision("0-0", PitchOutcome.BALL),
                ],
            ),
            PlateAppearance(
                batter_name="Mike Jones",
                baseball_event=BaseballEvent(
                    primary_event=EventType.SINGLE,
                    secondary_events=[],
                ),
                pitches=[
                    PitchDecision("0-0", PitchOutcome.BIP),
                ],
            ),
        ]
    )

    stats = aggregate_swing_decisions(game)

    assert stats["John Smith"]["0-0"]["PA"] == 1
    assert stats["John Smith"]["0-0"]["BALL"] == 1

    assert stats["Mike Jones"]["0-0"]["PA"] == 1
    assert stats["Mike Jones"]["0-0"]["BIP"] == 1