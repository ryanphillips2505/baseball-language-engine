from aggregators.game_stat_aggregator import aggregate_game_stats
from assemblers.plate_appearance_builder import build_plate_appearance
from models.game import Game


def test_gamechanger_bunts_out_to_catcher_counts_as_legacy_bunt_c():
    text = "Kaylee Baxter bunts out, catcher Kayla Orton to first baseman Kaelyn Staden."

    pa = build_plate_appearance(text)
    stats = aggregate_game_stats(Game([pa]))

    assert pa.batter_name == "Kaylee Baxter"
    assert pa.is_bip is True
    assert pa.ball_type == "BUNT"
    assert pa.location == "C"

    assert stats["Kaylee Baxter"]["BIP"] == 1
    assert stats["Kaylee Baxter"]["BUNT"] == 1
    assert stats["Kaylee Baxter"]["FB"] == 0
