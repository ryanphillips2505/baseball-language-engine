from cleaners.iscore_cleaner import clean_iscore_text
from dataset.sample_paths import sample_path
from language.reader import build_multi_platform_plate_appearance


def test_iscore_dataset_regression():
    raw_text = sample_path(
        "iscore",
        "iscore_raw_game_01.txt",
    ).read_text()

    cleaned_blocks = clean_iscore_text(raw_text)

    valid_events = []

    for block in cleaned_blocks:
        # iScore reads through BLE's multi-platform reader.
        baseball_event = build_multi_platform_plate_appearance(block).baseball_event

        assert baseball_event is not None
        valid_events.append(baseball_event)

    # 63: the cleaner also keeps "is intentionally walked" (2), "is picked
    # off" (1) and "is hit by the ball and called out" (1).
    assert len(cleaned_blocks) == 63
    assert len(valid_events) == 63