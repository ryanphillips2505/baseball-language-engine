from dataset.loader import load_pa_blocks
from detectors.event_detector import detect_event_types

blocks = load_pa_blocks("samples/gamechanger_pa_blocks.txt")

for block in blocks[:10]:
    print("=" * 50)
    print(detect_event_types(block))
