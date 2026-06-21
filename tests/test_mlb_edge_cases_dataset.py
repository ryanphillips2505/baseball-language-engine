from pathlib import Path

from cleaners.mlb_cleaner import clean_mlb_text


SAMPLE_PATH = Path(
    "samples/mlb/mlb_redsox_mariners_2026_06_20.txt"
)


def test_mlb_edge_cases_preserves_key_batter_events():
    raw_text = SAMPLE_PATH.read_text(encoding="utf-8")

    cleaned = clean_mlb_text(raw_text)

    assert any("called out on strikes" in line.lower() for line in cleaned)
    assert any("strikes out swinging" in line.lower() for line in cleaned)
    assert any("strikes out on a foul tip" in line.lower() for line in cleaned)
    assert any("grounds into a double play" in line.lower() for line in cleaned)
    assert any("out on a sacrifice fly" in line.lower() for line in cleaned)


def test_mlb_edge_cases_preserves_runner_and_error_events():
    raw_text = SAMPLE_PATH.read_text(encoding="utf-8")

    cleaned = clean_mlb_text(raw_text)

    assert any("caught stealing 2nd base" in line.lower() for line in cleaned)
    assert any("wild pitch by pitcher" in line.lower() for line in cleaned)
    assert any("throwing error by right fielder" in line.lower() for line in cleaned)


def test_mlb_edge_cases_preserves_batted_ball_types():
    raw_text = SAMPLE_PATH.read_text(encoding="utf-8")

    cleaned = clean_mlb_text(raw_text)

    assert any("flies out" in line.lower() for line in cleaned)
    assert any("grounds out" in line.lower() for line in cleaned)
    assert any("lines out" in line.lower() for line in cleaned)
    assert any("pops out" in line.lower() for line in cleaned)
    assert any("homers" in line.lower() for line in cleaned)