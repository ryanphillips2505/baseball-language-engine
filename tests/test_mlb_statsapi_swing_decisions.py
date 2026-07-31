from __future__ import annotations

from pathlib import Path

from aggregators.swing_decision_aggregator import aggregate_swing_decisions
from assemblers.pitch_decision_builder import (
    build_pitch_decisions_from_pitch_events,
)
from classifiers.statsapi_pitch_decision_classifier import (
    classify_statsapi_pitch_result,
)
from models.pitch_decision import PitchDecision, PitchOutcome
from models.pitch_event import PitchEvent
from pipeline.process_game import process_game


ANGELS_ATHLETICS = Path(
    "samples/mlb/statsapi/raw/mlb_angels_athletics_2026_06_20_gamepk824988.live.json"
)
RED_SOX_ANGELS_GAMEDAY = Path(
    "samples/mlb/validation/red_sox_angels_2026_07_04.txt"
)


def test_classify_statsapi_pitch_results_from_fixture_vocabulary():
    assert classify_statsapi_pitch_result("Ball") == PitchOutcome.BALL
    assert classify_statsapi_pitch_result("Ball In Dirt") == PitchOutcome.BALL
    assert (
        classify_statsapi_pitch_result("Called Strike")
        == PitchOutcome.CALLED_STRIKE
    )
    assert (
        classify_statsapi_pitch_result("Swinging Strike")
        == PitchOutcome.SWING_MISS
    )
    assert (
        classify_statsapi_pitch_result("Swinging Strike (Blocked)")
        == PitchOutcome.SWING_MISS
    )
    assert classify_statsapi_pitch_result("Foul") == PitchOutcome.FOUL
    assert classify_statsapi_pitch_result("Foul Tip") == PitchOutcome.FOUL
    assert classify_statsapi_pitch_result("Foul Bunt") == PitchOutcome.FOUL
    assert (
        classify_statsapi_pitch_result("In play, out(s)") == PitchOutcome.BIP
    )
    assert (
        classify_statsapi_pitch_result("In play, no out") == PitchOutcome.BIP
    )
    assert (
        classify_statsapi_pitch_result(
            "In play, run(s)",
            ball_in_play=True,
        )
        == PitchOutcome.BIP
    )
    assert classify_statsapi_pitch_result("Hit By Pitch") is None


def test_jose_siri_sacrifice_fly_pitch_decisions():
    game = process_game(ANGELS_ATHLETICS.read_text(encoding="utf-8"))

    matching = [
        pa
        for pa in game.plate_appearances
        if pa.batter_name == "Jose Siri"
        and pa.baseball_event is not None
        and pa.baseball_event.primary_event.value == "sac_fly"
    ]
    assert len(matching) == 1
    assert matching[0].pitches == [
        PitchDecision("0-0", PitchOutcome.FOUL),
        PitchDecision("0-1", PitchOutcome.BALL),
        PitchDecision("1-1", PitchOutcome.BALL),
        PitchDecision("2-1", PitchOutcome.BALL),
        PitchDecision("3-1", PitchOutcome.FOUL),
        PitchDecision("3-2", PitchOutcome.BIP),
    ]


def test_statsapi_swing_aggregator_covers_mappable_pitches():
    game = process_game(ANGELS_ATHLETICS.read_text(encoding="utf-8"))
    totals = aggregate_swing_decisions(game)

    assert totals
    assert "Jose Siri" in totals

    outcome_sum = 0
    for player_counts in totals.values():
        for bucket in player_counts.values():
            outcome_sum += (
                bucket["BIP"]
                + bucket["SWING_MISS"]
                + bucket["FOUL"]
                + bucket["CALLED_STRIKE"]
                + bucket["BALL"]
            )

    # Angels @ Athletics has 322 isPitch events and 1 HBP (skipped).
    assert len(game.pitch_events) == 322
    hbp = sum(
        1
        for pitch in game.pitch_events
        if pitch.result.lower() == "hit by pitch"
    )
    assert hbp == 1
    assert outcome_sum == 321

    pa_decisions = sum(len(pa.pitches) for pa in game.plate_appearances)
    assert pa_decisions == 321
    assert all(
        isinstance(pitch, PitchDecision)
        for pa in game.plate_appearances
        for pitch in pa.pitches
    )


def test_build_pitch_decisions_from_pitch_events_skips_hbp():
    pitches = [
        PitchEvent(
            pitch_number=1,
            count_before="0-0",
            result="Ball",
            swing=False,
        ),
        PitchEvent(
            pitch_number=2,
            count_before="1-0",
            result="Hit By Pitch",
            swing=False,
        ),
        PitchEvent(
            pitch_number=3,
            count_before="1-0",
            result="Called Strike",
            swing=False,
        ),
    ]
    assert build_pitch_decisions_from_pitch_events(pitches) == [
        PitchDecision("0-0", PitchOutcome.BALL),
        PitchDecision("1-0", PitchOutcome.CALLED_STRIKE),
    ]


def test_gameday_text_path_still_does_not_invent_statsapi_swing_sequences():
    game = process_game(RED_SOX_ANGELS_GAMEDAY.read_text(encoding="utf-8"))

    # Gameday paste has no playEvents; do not invent structured pitch feeds.
    assert game.pitch_events == []

    # Description text may still yield rare incidental FOUL tokens
    # ("foul tip" / "foul territory"); those are not StatsAPI sequences.
    assert all(len(pa.pitches) <= 1 for pa in game.plate_appearances)
    assert all(
        pitch.outcome == PitchOutcome.FOUL
        for pa in game.plate_appearances
        for pitch in pa.pitches
    )
