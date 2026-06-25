from pathlib import Path

from aggregators.swing_decision_aggregator import aggregate_swing_decisions
from assemblers.gamechanger_swing_game_builder import build_gamechanger_swing_game


SAMPLE_PATH = Path(
    "samples/gamechanger/risin_shockers_2026_06_04.txt"
)


def test_opponent_iq_swing_parity_game_01():
    raw_text = SAMPLE_PATH.read_text(encoding="utf-8")
    game = build_gamechanger_swing_game(raw_text)
    stats = aggregate_swing_decisions(game)

    players = [
        "Wade Webb",
        "Miles Stanley",
        "Traylon Barnes",
        "Wyatt Jones",
        "Rylan Kuklinski",
        "Charles Copus",
        "Kellen Smith",
    ]

    for player in players:
        print(f"\n{player}:")
        for count, bucket in stats[player].items():
            if any(bucket.values()):
                print(count, bucket)

    assert stats