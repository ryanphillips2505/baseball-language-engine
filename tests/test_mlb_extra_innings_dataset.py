from cleaners.mlb_cleaner import clean_mlb_text
from dataset.sample_paths import sample_path


SAMPLE_PATH = sample_path(
    "mlb",
    "mlb_athletics_angels_2026_06_20.txt",
)


def test_mlb_extra_innings_preserves_pickoff_and_caught_stealing():
    raw_text = SAMPLE_PATH.read_text(encoding="utf-8")

    cleaned = clean_mlb_text(raw_text)

    assert any(
        "picked off and caught stealing 2nd base" in line.lower()
        for line in cleaned
    )
    assert any("caught stealing 2nd" in line.lower() for line in cleaned)


def test_mlb_extra_innings_preserves_compound_strikeout_double_play():
    raw_text = SAMPLE_PATH.read_text(encoding="utf-8")

    cleaned = clean_mlb_text(raw_text)

    assert any(
        "strikes out on a foul tip" in line.lower()
        and "caught stealing 2nd" in line.lower()
        for line in cleaned
    )


def test_mlb_extra_innings_preserves_runner_placed_on_base():
    raw_text = SAMPLE_PATH.read_text(encoding="utf-8")

    cleaned = clean_mlb_text(raw_text)

    assert any(
        "starts inning at 2nd base" in line.lower()
        for line in cleaned
    )


def test_mlb_extra_innings_preserves_fielders_choice_out():
    raw_text = SAMPLE_PATH.read_text(encoding="utf-8")

    cleaned = clean_mlb_text(raw_text)

    assert any(
        "fielder's choice out" in line.lower()
        for line in cleaned
    )


def test_mlb_extra_innings_preserves_double_steal_and_walkoff_walk():
    raw_text = SAMPLE_PATH.read_text(encoding="utf-8")

    cleaned = clean_mlb_text(raw_text)

    assert any("steals (5) 3rd base" in line.lower() for line in cleaned)
    assert any("steals (7) 2nd base" in line.lower() for line in cleaned)
    assert any(
        "walks. lawrence butler scores" in line.lower()
        for line in cleaned
    )