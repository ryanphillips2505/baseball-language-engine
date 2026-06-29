from pathlib import Path

from aggregators.game_stat_aggregator import aggregate_game_stats
from pipeline.process_game import process_game


SAMPLE_PATH = Path("samples/college/raw/college_raw_game_01.txt")


def test_college_stats_sample_exists():
    assert SAMPLE_PATH.exists()


def test_college_stats_builds_player_stats():
    raw_text = SAMPLE_PATH.read_text(encoding="utf-8")

    game = process_game(raw_text)

    stats = aggregate_game_stats(game)

    assert isinstance(stats, dict)
    assert len(stats) > 0


def test_college_stats_tracks_games_played():
    raw_text = SAMPLE_PATH.read_text(encoding="utf-8")

    game = process_game(raw_text)

    stats = aggregate_game_stats(game)

    for player in stats.values():
        assert player["GP"] >= 1
        