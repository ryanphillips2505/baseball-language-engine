from pathlib import Path

from cleaners.gamechanger_cleaner import clean_gamechanger_text


SAMPLE_PATH = Path("samples/gamechanger/gc_17_games_yukon_2026.txt")


def test_gc_17_game_sample_file_exists():
    assert SAMPLE_PATH.exists()


def test_gc_17_game_cleaner_produces_large_validation_set():
    raw_text = SAMPLE_PATH.read_text(encoding="utf-8")

    cleaned = clean_gamechanger_text(raw_text)

    assert len(cleaned) >= 300


def test_gc_17_game_cleaner_preserves_core_events():
    raw_text = SAMPLE_PATH.read_text(encoding="utf-8")

    cleaned = clean_gamechanger_text(raw_text)
    combined = "\n".join(cleaned).lower()

    assert "strikes out swinging" in combined
    assert "strikes out looking" in combined
    assert "walks" in combined
    assert "is hit by pitch" in combined

    assert "singles" in combined
    assert "doubles" in combined
    assert "triples" in combined
    assert "homers" in combined

    assert "grounds out" in combined
    assert "flies out" in combined
    assert "lines out" in combined
    assert "pops out" in combined

    assert "reaches on an error" in combined
    assert "fielder's choice" in combined
    assert "double play" in combined
    assert "sacrifice fly" in combined
    assert "sacrifices" in combined or "bunts out" in combined

    assert "steals 2nd" in combined
    assert "caught stealing" in combined
    assert "wild pitch" in combined
    assert "passed ball" in combined
    assert "dropped 3rd strike" in combined or "foul tip" in combined