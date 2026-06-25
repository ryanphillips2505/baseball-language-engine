from translators.player_card_translator import build_player_card, build_player_cards


def test_build_player_card():
    game_stats = {
        "Wade Webb": {
            "GP": 1,
            "K": 0,
            "BB": 0,
            "HBP": 0,
            "2B": 1,
            "3B": 1,
            "HR": 0,
            "XBH": 2,
            "SB": 0,
            "CS": 0,
            "BIP": 3,
            "GB": 0,
            "FB": 3,
            "BUNT": 0,
            "LOC_LF": 1,
            "LOC_CF": 2,
            "LOC_RF": 0,
            "LOC_3B": 0,
            "LOC_SS": 0,
            "LOC_2B": 0,
            "LOC_1B": 0,
            "LOC_P": 0,
            "XBH_LF": 0,
            "XBH_CF": 2,
            "XBH_RF": 0,
            "XBH_UNKNOWN": 0,
        }
    }

    swing_stats = {
        "Wade Webb": {
            "0-0": {
                "PA": 3,
                "BIP": 0,
                "SWING_MISS": 0,
                "FOUL": 1,
                "CALLED_STRIKE": 1,
                "BALL": 1,
            }
        }
    }

    card = build_player_card("Wade Webb", game_stats, swing_stats)

    assert card["Player"] == "Wade Webb"

    assert card["Season Summary"]["GP"] == 1
    assert card["Season Summary"]["2B"] == 1
    assert card["Season Summary"]["3B"] == 1
    assert card["Season Summary"]["XBH"] == 2
    assert card["Season Summary"]["BIP"] == 3

    assert card["Spray Zone"]["LOC_LF"] == 1
    assert card["Spray Zone"]["LOC_CF"] == 2
    assert card["Spray Zone"]["FB"] == 3

    assert card["Damage"]["XBH"] == 2
    assert card["Damage"]["XBH_CF"] == 2

    assert card["Swing Decision"]["0-0"]["PA"] == 3
    assert card["Swing Decision"]["0-0"]["FOUL"] == 1


def test_build_player_cards_ignores_blank_names():
    game_stats = {
        "Wade Webb": {"GP": 1},
        "": {"GP": 1},
    }

    cards = build_player_cards(game_stats)

    assert len(cards) == 1
    assert cards[0]["Player"] == "Wade Webb"
    