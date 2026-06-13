from cleaners.mlb_cleaner import clean_mlb_text

raw_text = """
PASTE A RAW MLB COPY/PASTE BLOCK HERE
"""

cleaned_blocks = clean_mlb_text(raw_text)

print(f"Cleaned blocks: {len(cleaned_blocks)}")

for index, block in enumerate(cleaned_blocks, start=1):
    print("=" * 70)
    print(f"PA #{index}")
    print(block)
