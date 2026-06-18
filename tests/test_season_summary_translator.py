from translators.season_summary_translator import build_season_summary_rows


def test_build_season_summary_rows():
    opponent_iq_stats = {
        "John Smith": {
            "hitting": {
                "GP": 1,
                "GB": 2,
                "FB": 1,
                "BIP": 3,
            },
            "locations": {
                "SS": 2,
            },
            "combos": {},
        }
    }

    rows = build_season_summary_rows(opponent_iq_stats)

    assert len(rows) == 1

    row = rows[0]

    assert row["Player"] == "John Smith"
    assert row["GP"] == 1
    assert row["SS"] == 2
    assert row["GB"] == 2
    assert row["FB"] == 1
    assert row["BIP"] == 3
    assert row["GB%"] == 66.7
    assert row["FB%"] == 33.3