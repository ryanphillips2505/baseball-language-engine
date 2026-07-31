from cleaners.mlb_cleaner import clean_mlb_text
from dataset.sample_paths import sample_path
from detectors.event_detector import detect_event_types
from translators.base_translator import detected_events_to_baseball_event


def test_mlb_dataset_regression():
    raw_text = sample_path(
        "mlb",
        "mlb_pa_blocks.txt",
    ).read_text()

    cleaned_blocks = clean_mlb_text(raw_text)

    valid_events = []

    for block in cleaned_blocks:
        detected = detect_event_types(block)
        baseball_event = detected_events_to_baseball_event(detected)

        assert baseball_event is not None
        valid_events.append(baseball_event)

    # Includes strikeout-swinging lines previously dropped by the highlight-caption
    # false positive ("strikes out swinging." matched as a video caption).
    assert len(cleaned_blocks) == 85
    assert len(valid_events) == 85