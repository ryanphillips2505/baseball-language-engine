from cleaners.college_cleaner import clean_college_text
from dataset.sample_paths import sample_path


SAMPLE_PATH = sample_path(
    "college",
    "espn_college_world_series_2026_unc_wvu.txt",
)


def test_espn_pitch_level_dataset_cleans_plate_appearance_results():
    raw_text = SAMPLE_PATH.read_text(encoding="utf-8")

    cleaned = clean_college_text(raw_text)

    assert "J. Schaffner walked." in cleaned
    assert "O. Hull doubled to deep right center, J. Schaffner scored." in cleaned
    assert "G. Gallaher grounded out to third." in cleaned
    assert "T. Howe struck out swinging." in cleaned
    assert "A. Guzman reached on bunt single to pitcher." in cleaned
    assert "P. Schoenfeld hit by pitch." in cleaned
    assert "G. Kelly homered to left." in cleaned


def test_espn_pitch_level_dataset_current_cleaner_drops_pitch_tokens():
    raw_text = SAMPLE_PATH.read_text(encoding="utf-8")

    cleaned = clean_college_text(raw_text)

    assert "Strike Looking" not in cleaned
    assert "Strike Swinging" not in cleaned
    assert "Foul Ball" not in cleaned