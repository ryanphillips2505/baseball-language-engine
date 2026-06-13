from cleaners.iscore_cleaner import clean_iscore_text
from detectors.event_detector import detect_event_types
from translators.base_translator import detected_events_to_baseball_event

raw_text = """
PASTE RAW ISCORE TEXT HERE
"""

cleaned_lines = clean_iscore_text(raw_text)

valid = 0
invalid = []

for index, line in enumerate(cleaned_lines, start=1):
    detected = detect_event_types(line)
    baseball_event = detected_events_to_baseball_event(detected)

    if baseball_event:
        valid += 1
    else:
        invalid.append((index, line))

print(f"Cleaned lines: {len(cleaned_lines)}")
print(f"Valid BaseballEvents: {valid}")
print(f"Invalid cleaned lines: {len(invalid)}")

for index, line in invalid:
    print("=" * 70)
    print(f"Line #{index}")
    print(line)
