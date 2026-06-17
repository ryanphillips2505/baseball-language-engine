from pathlib import Path

from aggregators.game_stat_aggregator import aggregate_game_stats
from assemblers.plate_appearance_builder import build_plate_appearance
from cleaners.gamechanger_cleaner import clean_gamechanger_text
from models.game import Game


raw_text = Path("samples/gamechanger_pa_blocks.txt").read_text()

cleaned_blocks = clean_gamechanger_text(raw_text)

game = Game(
    plate_appearances=[
        build_plate_appearance(block)
        for block in cleaned_blocks
    ]
)

stats = aggregate_game_stats(game)

print("CLEANED BLOCKS:", len(cleaned_blocks))
print("PLAYERS:", len(stats))
print()

for player, player_stats in sorted(stats.items()):
    print(player)
    print(player_stats)
    print()
