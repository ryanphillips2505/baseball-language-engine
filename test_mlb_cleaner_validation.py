from cleaners.mlb_cleaner import clean_mlb_text
from detectors.event_detector import detect_event_types
from translators.base_translator import detected_events_to_baseball_event

raw_text = """
PASTE FULL RAW MLB COPY/PASTE HERE
"""

blocks = clean_mlb_text(raw_text)

valid = 0
invalid = []

for index, block in enumerate(blocks, start=1):
    detected = detect_event_types(block)
    event = detected_events_to_baseball_event(detected)

    if event:
        valid += 1
    else:
        invalid.append((index, block))

print(f"Cleaned blocks: {len(blocks)}")
print(f"Valid BaseballEvents: {valid}")
print(f"Invalid cleaned blocks: {len(invalid)}")

for index, block in invalid:
    print("=" * 70)
    print(f"PA #{index}")
    print(block)