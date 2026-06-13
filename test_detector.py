from dataset.loader import load_pa_blocks
from detectors.event_detector import detect_event_types

blocks = load_pa_blocks("samples/gamechanger_pa_blocks.txt")

for index, block in enumerate(blocks[:30], start=1):
    print("=" * 70)
    print(f"PA #{index}")
    print("-" * 70)
    print(block)
    print("-" * 70)
    print("Detected:")
    print(detect_event_types(block))
