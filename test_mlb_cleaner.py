from cleaners.mlb_cleaner import clean_mlb_text

raw_text = """
Top 1st
Fernando Tatis Jr. headshot
Single
Fernando Tatis Jr. singles...
00:13
Exit Velocity
103.4 mph
Distance
418 ft
Launch Angle
27 deg

Manny Machado headshot
Flyout
Manny Machado flies out...
Win Probability
74.1%
"""

cleaned_blocks = clean_mlb_text(raw_text)

print(f"Cleaned blocks: {len(cleaned_blocks)}")

for index, block in enumerate(cleaned_blocks, start=1):
    print("=" * 70)
    print(f"PA #{index}")
    print(block)