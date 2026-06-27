from cleaners.iscore_cleaner import clean_iscore_text
from dataset.sample_paths import sample_path


SAMPLE_PATH = sample_path(
    "iscore",
    "iscore_edge_cases_2026_yukon.txt",
)


def test_iscore_edge_cases_preserves_key_batter_events():
    raw_text = SAMPLE_PATH.read_text(encoding="utf-8")

    cleaned = clean_iscore_text(raw_text)

    assert any("ground rule double" in line.lower() for line in cleaned)
    assert any("sacrifice fly" in line.lower() for line in cleaned)
    assert any("line drive" in line.lower() for line in cleaned)
    assert any("bunts for an out" in line.lower() for line in cleaned)
    assert any("homerun" in line.lower() for line in cleaned)


def test_iscore_edge_cases_preserves_runner_and_error_events():
    raw_text = SAMPLE_PATH.read_text(encoding="utf-8")

    cleaned = clean_iscore_text(raw_text)

    assert any("steals third" in line.lower() for line in cleaned)
    assert any("forced out at home" in line.lower() for line in cleaned)
    assert any("error" in line.lower() for line in cleaned)
    assert any("scores" in line.lower() for line in cleaned)


def test_iscore_edge_cases_preserves_strikeout_types():
    raw_text = SAMPLE_PATH.read_text(encoding="utf-8")

    cleaned = clean_iscore_text(raw_text)

    assert any("strikes out swinging" in line.lower() for line in cleaned)
    assert any("strikes out looking" in line.lower() for line in cleaned)