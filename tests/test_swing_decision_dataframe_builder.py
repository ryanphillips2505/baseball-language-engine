from translators.swing_decision_dataframe_builder import (
    build_swing_decision_dataframe,
)


def test_build_swing_decision_dataframe():
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

    df = build_swing_decision_dataframe(swing_stats)

    assert not df.empty

    assert "Count" in df.columns
    assert "BIP %" in df.columns
    assert "Swing and Miss %" in df.columns
    assert "Foul %" in df.columns
    assert "Called Strike %" in df.columns
    assert "Ball %" in df.columns
    assert "Total PA" in df.columns

    assert df.iloc[0]["Count"] == "TEAM TOTAL"
    