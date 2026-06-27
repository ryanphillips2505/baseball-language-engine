from dataset.sample_paths import sample_path
from detectors.source_detector import SourceType, detect_source


def test_detects_real_gamechanger_sample():
    raw_text = sample_path(
        "gamechanger",
        "gamechanger_pa_blocks.txt",
    ).read_text()

    assert detect_source(raw_text) == SourceType.GAMECHANGER


def test_detects_real_iscore_sample():
    raw_text = sample_path(
        "iscore",
        "iscore_raw_game_01.txt",
    ).read_text()

    assert detect_source(raw_text) == SourceType.ISCORE


def test_detects_real_mlb_sample():
    raw_text = sample_path(
        "mlb",
        "mlb_pa_blocks.txt",
    ).read_text()

    assert detect_source(raw_text) == SourceType.MLB


def test_detects_real_college_sample():
    raw_text = sample_path(
        "college",
        "college_raw_game_01.txt",
    ).read_text()

    assert detect_source(raw_text) == SourceType.COLLEGE