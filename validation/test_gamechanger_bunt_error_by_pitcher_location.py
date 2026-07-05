from assemblers.plate_appearance_builder import build_plate_appearance
from aggregators.game_stat_aggregator import aggregate_game_stats
from models.game import Game
from models.types import EventType


def test_gamechanger_bunts_and_reaches_error_by_pitcher_understands_bunt_to_pitcher_error():
    text = (
        "Kate Seaton bunts and reaches on an error by pitcher Grace Tonga, "
        "Ryen Bullock scores."
    )

    pa = build_plate_appearance(text)

    assert pa.batter_name == "Kate Seaton"
    assert pa.is_bip is True
    assert pa.ball_type == "BUNT"
    assert pa.location == "P"
    assert pa.baseball_event.primary_event == EventType.ERROR


def test_gamechanger_bunts_and_reaches_error_by_pitcher_counts_bunt_and_pitcher_location():
    text = (
        "Kate Seaton bunts and reaches on an error by pitcher Grace Tonga, "
        "Ryen Bullock scores."
    )

    pa = build_plate_appearance(text)
    stats = aggregate_game_stats(Game([pa]))

    assert stats["Kate Seaton"]["BIP"] == 1
    assert stats["Kate Seaton"]["BUNT"] == 1
    assert stats["Kate Seaton"]["LOC_P"] == 1
    assert stats["Kate Seaton"]["BUNT-LOC_P"] == 1

def test_gamechanger_hits_ground_ball_reaches_error_by_pitcher_counts_ground_ball_pitcher_location():
    text = (
        "Drake Pace hits a ground ball and reaches on an error by pitcher Noah Burns, "
        "Eddie Fish scores, Drake Pace advances to 2nd on the same error."
    )

    pa = build_plate_appearance(text)
    stats = aggregate_game_stats(Game([pa]))

    assert pa.batter_name == "Drake Pace"
    assert pa.is_bip is True
    assert pa.ball_type == "GB"
    assert pa.location == "P"
    assert pa.baseball_event.primary_event == EventType.ERROR

    assert stats["Drake Pace"]["BIP"] == 1
    assert stats["Drake Pace"]["GB"] == 1
    assert stats["Drake Pace"]["LOC_P"] == 1
    assert stats["Drake Pace"]["GB-LOC_P"] == 1

