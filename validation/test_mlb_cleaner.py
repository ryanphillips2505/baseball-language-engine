from pathlib import Path

from cleaners.mlb_cleaner import clean_mlb_text


SAMPLE_PATHS = [
    Path("samples/mlb/raw/mlb_pa_blocks.txt"),
    Path("samples/mlb/raw/mlb_athletics_angels_2026_06_20.txt"),
    Path("samples/mlb/raw/mlb_redsox_mariners_2026_06_20.txt"),
]


def test_mlb_sample_files_exist():
    for path in SAMPLE_PATHS:
        assert path.exists()


def test_mlb_cleaner_preserves_core_events():
    combined = []

    for path in SAMPLE_PATHS:
        raw_text = path.read_text(encoding="utf-8")
        cleaned = clean_mlb_text(raw_text)
        combined.extend(cleaned)

    text = "\n".join(combined).lower()

    assert "single" in text or "singles" in text
    assert "double" in text or "doubles" in text
    assert "triple" in text or "triples" in text
    assert "home run" in text or "homers" in text

    assert "ground" in text
    assert "fly" in text
    assert "line" in text

    assert "walk" in text
    assert "strike" in text