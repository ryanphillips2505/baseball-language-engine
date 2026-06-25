from pathlib import Path

from adapters.opponent_iq_adapter import adapt_game_stats_to_opponent_iq
from aggregators.game_stat_aggregator import aggregate_game_stats
from assemblers.plate_appearance_builder import build_plate_appearance
from cleaners.gamechanger_cleaner import clean_gamechanger_text
from models.game import Game


SAMPLE_PATH = Path(
    "samples/gamechanger/risin_shockers_2026_06_04.txt"
)


def build_game_from_gc_text(raw_text: str) -> Game:
    cleaned_blocks = clean_gamechanger_text(raw_text)

    plate_appearances = [
        build_plate_appearance(block)
        for block in cleaned_blocks
    ]

    return Game(
        plate_appearances=plate_appearances
    )


def test_risin_shockers_game_runs_through_engine():
    raw_text = SAMPLE_PATH.read_text(encoding="utf-8")

    game = build_game_from_gc_text(raw_text)

    game_stats = aggregate_game_stats(game)
    opponent_iq_stats = adapt_game_stats_to_opponent_iq(game_stats)

    assert opponent_iq_stats


def test_risin_shockers_key_risin_players_present():
    raw_text = SAMPLE_PATH.read_text(encoding="utf-8")

    game = build_game_from_gc_text(raw_text)

    game_stats = aggregate_game_stats(game)
    stats = adapt_game_stats_to_opponent_iq(game_stats)

    expected_players = {
        "Wade Webb",
        "Miles Stanley",
        "Blake Ridley",
        "Traylon Barnes",
        "Wyatt Jones",
        "Rylan Kuklinski",
        "Charles Copus",
        "Kellen Smith",
        "Drake Pace",
        "Jefferson Hodge",
    }

    missing = expected_players - set(stats.keys())

    assert missing == set()


def test_risin_shockers_known_risin_results():
    raw_text = SAMPLE_PATH.read_text(encoding="utf-8")

    game = build_game_from_gc_text(raw_text)

    game_stats = aggregate_game_stats(game)
    stats = adapt_game_stats_to_opponent_iq(game_stats)

    assert stats["Traylon Barnes"]["HR"] >= 1
    assert stats["Miles Stanley"]["HR"] >= 1
    print(stats["Wade Webb"])
    assert stats["Wade Webb"]["2B"] >= 1
    assert stats["Wade Webb"]["3B"] >= 1

