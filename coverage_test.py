from dataset.loader import load_pa_blocks
from detectors.event_detector import detect_event_types

blocks = load_pa_blocks("samples/gamechanger_pa_blocks.txt")

detected_count = 0
undetected_blocks = []

for index, block in enumerate(blocks, start=1):
    events = detect_event_types(block)

    if events:
        detected_count += 1
    else:
        undetected_blocks.append((index, block))

print(f"Total PA blocks: {len(blocks)}")
print(f"Detected PA blocks: {detected_count}")
print(f"Undetected PA blocks: {len(undetected_blocks)}")
print(f"Coverage: {detected_count / len(blocks):.1%}")

print("\nUndetected Blocks:")
for index, block in undetected_blocks:
    print("=" * 70)
    print(f"PA #{index}")
    print(block)
