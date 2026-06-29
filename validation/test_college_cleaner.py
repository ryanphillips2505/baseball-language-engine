from pathlib import Path

from cleaners.college_cleaner import clean_college_text


SAMPLE_PATHS = [
    Path("samples/college/raw/college_raw_game_01.txt"),
    Path("samples/college/raw/espn_college_world_series_2026_unc_wvu.txt"),
    Path("samples/college/raw/espn_ou_vs_unc_2026_cws.txt"),
]


def test_college_sample_files_exist():
    for path in SAMPLE_PATHS:
        assert path.exists()


def test_college_cleaner_preserves_core_events():
    combined = []

    for path in SAMPLE_PATHS:
        raw_text = path.read_text(encoding="utf-8")
        cleaned = clean_college_text(raw_text)
        combined.extend(cleaned)

    text = "\n".join(combined).lower()

    assert "singled" in text or "singles" in text
    assert "doubled" in text or "doubles" in text
    assert "tripled" in text or "triples" in text
    assert "homered" in text or "home run" in text

    assert "grounded" in text or "grounds" in text
    assert "flied" in text or "flies" in text
    assert "lined" in text or "lines" in text

    assert "walked" in text or "walks" in text
    assert "struck out" in text or "strikes out" in text