from translators.damage_dataframe_builder import build_damage_dataframe


def test_build_damage_dataframe():
    rows = [
        {
            "Player": "John Smith",
            "GP": 1,
            "XBH_LF": 2,
            "XBH_CF": 1,
            "XBH_RF": 3,
            "XBH": 99,
        }
    ]

    df = build_damage_dataframe(rows)

    assert len(df) == 1

    row = df.iloc[0]

    assert row["Player"] == "John Smith"
    assert row["GP"] == 1
    assert row["XBH_LF"] == 2
    assert row["XBH_CF"] == 1
    assert row["XBH_RF"] == 3
    assert row["XBH"] == 6