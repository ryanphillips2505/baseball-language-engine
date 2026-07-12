from aggregators.game_stat_aggregator import aggregate_game_stats
from assemblers.plate_appearance_builder import build_plate_appearance
from models.game import Game
from models.types import EventType


def test_espn_foul_bunt_strikeout_is_k_not_bunt_or_bip():
    text = "M. Winslow struck out bunting foul."

    pa = build_plate_appearance(text)
    stats = aggregate_game_stats(Game([pa]))
    player = stats["M. Winslow"]

    assert pa.batter_name == "M. Winslow"
    assert pa.baseball_event is not None
    assert (
        pa.baseball_event.primary_event
        == EventType.STRIKEOUT_SWINGING
    )

    assert pa.is_bip is False
    assert pa.ball_type is None
    assert pa.location is None

    assert player["K"] == 1
    assert player["BUNT"] == 0
    assert player["BIP"] == 0
