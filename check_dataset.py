from dataset.loader import load_pa_blocks


blocks = load_pa_blocks("samples/gamechanger_pa_blocks.txt")

print(f"Loaded PA blocks: {len(blocks)}")
print()
print("First PA block:")
print(blocks[0])
