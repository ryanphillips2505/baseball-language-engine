from translators.season_summary_dataframe_builder import (
    build_season_summary_dataframe,
)


def test_build_season_summary_dataframe():
    rows = [
        {
            "Player": "John Smith",
            "GP": 1,
            "GB": 2,
            "FB": 1,
            "GB-SS": 2,
            "FB-RF": 1,
            "BUNT": 0,
            "K": 1,
            "BB": 2,
            "SB": 1,
            "CS": 0,
        }
    ]

    df = build_season_summary_dataframe(rows)

    assert len(df) == 1

    row = df.iloc[0]

    assert row["Player"] == "John Smith"
    assert row["GP"] == 1
    assert row["GB%"] == 2 / 3
    assert row["FB%"] == 1 / 3
    assert row["GB-SS"] == 2 / 3
    assert row["FB-RF"] == 1 / 3
    assert row["BIP"] == 3
    assert row["K"] == 1
    assert row["BB"] == 2
    assert row["SB"] == 1
    assert row["CS"] == 0