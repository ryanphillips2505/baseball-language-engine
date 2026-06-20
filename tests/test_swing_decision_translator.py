from translators.swing_decision_translator import build_swing_decision_rows


def test_builds_swing_decision_rows_with_percentages():
    swing_stats = {
        "John Smith": {
            "0-0": {
                "PA": 4,
                "BIP": 1,
                "SWING_MISS": 1,
                "FOUL": 1,
                "CALLED_STRIKE": 0,
                "BALL": 1,
            },
            **{
                count: {
                    "PA": 0,
                    "BIP": 0,
                    "SWING_MISS": 0,
                    "FOUL": 0,
                    "CALLED_STRIKE": 0,
                    "BALL": 0,
                }
                for count in [
                    "1-0",
                    "0-1",
                    "2-0",
                    "1-1",
                    "0-2",
                    "3-0",
                    "2-1",
                    "1-2",
                    "3-1",
                    "2-2",
                    "3-2",
                ]
            },
        }
    }

    rows = build_swing_decision_rows(swing_stats)

    first = rows[0]

    assert first["Player"] == "John Smith"
    assert first["Count"] == "0-0"
    assert first["BIP %"] == 0.25
    assert first["Swing and Miss %"] == 0.25
    assert first["Foul %"] == 0.25
    assert first["Called Strike %"] == 0.0
    assert first["Ball %"] == 0.25
    assert first["Total PA"] == 4