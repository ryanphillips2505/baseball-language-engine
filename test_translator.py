from dataset.loader import load_pa_blocks
from detectors.event_detector import detect_event_types
from translators.base_translator import detected_events_to_baseball_event

blocks = load_pa_blocks("samples/gamechanger_pa_blocks.txt")

for index, block in enumerate(blocks[:30], start=1):
    detected = detect_event_types(block)
    baseball_event = detected_events_to_baseball_event(detected)

    print("=" * 70)
    print(f"PA #{index}")
    print(block)
    print("-" * 70)
    print(baseball_event)
