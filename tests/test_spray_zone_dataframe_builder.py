from translators.spray_zone_dataframe_builder import build_spray_zone_dataframe


def test_build_spray_zone_dataframe():
    rows = [
        {
            "Player": "John Smith",
            "LF": 3,
            "CF": 4,
            "RF": 2,
            "3B/SS": 4,
            "2B/1B": 5,
            "BIP": 18,
        }
    ]

    df = build_spray_zone_dataframe(rows)

    assert len(df) == 1

    row = df.iloc[0]

    assert row["Player"] == "John Smith"
    assert row["LF"] == 3
    assert row["CF"] == 4
    assert row["RF"] == 2
    assert row["3B/SS"] == 4
    assert row["2B/1B"] == 5
    assert row["BIP"] == 18