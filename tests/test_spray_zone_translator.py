from translators.spray_zone_translator import build_spray_zone_rows


def test_build_spray_zone_rows():
    season_summary_rows = [
        {
            "Player": "John Smith",
            "GB-LF": 1,
            "FB-LF": 2,
            "GB-CF": 3,
            "FB-CF": 1,
            "GB-RF": 2,
            "FB-RF": 0,
            "GB-3B": 1,
            "FB-3B": 1,
            "GB-SS": 2,
            "FB-SS": 0,
            "GB-2B": 1,
            "FB-2B": 1,
            "GB-1B": 2,
            "FB-1B": 1,
        }
    ]

    rows = build_spray_zone_rows(season_summary_rows)

    assert len(rows) == 1

    row = rows[0]

    assert row["Player"] == "John Smith"
    assert row["LF"] == 3
    assert row["CF"] == 4
    assert row["RF"] == 2
    assert row["3B/SS"] == 4
    assert row["2B/1B"] == 5
    assert row["BIP"] == 18