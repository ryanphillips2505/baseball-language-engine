from pathlib import Path

from cleaners.iscore_cleaner import clean_iscore_text


SAMPLE_PATHS = [
    Path("samples/iscore/raw/iscore_raw_game_01.txt"),
    Path("samples/iscore/raw/iscore_edge_cases_2026_yukon.txt"),
]


def test_iscore_sample_files_exist():
    for path in SAMPLE_PATHS:
        assert path.exists()


def test_iscore_cleaner_preserves_core_events():
    combined = []

    for path in SAMPLE_PATHS:
        raw_text = path.read_text(encoding="utf-8")
        cleaned = clean_iscore_text(raw_text)
        combined.extend(cleaned)

    text = "\n".join(combined).lower()

    assert "single" in text or "hits" in text
    assert "double" in text or "triple" in text
    assert "ground" in text
    assert "fly" in text or "line" in text
    assert "walk" in text
    assert "strike" in text