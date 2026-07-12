from aggregators.game_stat_aggregator import aggregate_game_stats
from assemblers.plate_appearance_builder import build_plate_appearance
from models.game import Game


def test_espn_strikeout_plus_caught_stealing_keeps_runner_identity():
    text = (
        "E. Paulsen struck out swinging. "
        "G. Gallaher caught stealing second, catcher to shortstop."
    )

    pa = build_plate_appearance(text)

    assert len(pa.runner_events) == 1

    runner = pa.runner_events[0]

    assert runner.event_type == "CS"
    assert runner.base == "2B"
    assert runner.runner_name == "G. Gallaher"

    stats = aggregate_game_stats(Game([pa]))

    assert stats["E. Paulsen"]["K"] == 1
    assert stats["G. Gallaher"]["CS"] == 1
    assert stats["G. Gallaher"]["CS-2B"] == 1
