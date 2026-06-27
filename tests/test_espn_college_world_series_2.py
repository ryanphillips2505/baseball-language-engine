from cleaners.college_cleaner import clean_college_text
from dataset.sample_paths import sample_path


SAMPLE_PATH = sample_path(
    "college",
    "espn_ou_vs_unc_2026_cws.txt",
)


def test_espn_cws_game_preserves_key_events():
    raw_text = SAMPLE_PATH.read_text(encoding="utf-8")

    cleaned = clean_college_text(raw_text)

    assert any("sacrifice fly" in line.lower() for line in cleaned)

    assert any("sacrifice bunt" in line.lower() for line in cleaned)

    assert any("grounded into double play" in line.lower() for line in cleaned)

    assert any("picked off and caught stealing" in line.lower() for line in cleaned)

    assert any("hit by pitch" in line.lower() for line in cleaned)


def test_espn_cws_game_preserves_runner_events():
    raw_text = SAMPLE_PATH.read_text(encoding="utf-8")

    cleaned = clean_college_text(raw_text)

    assert any("stole second" in line.lower() for line in cleaned)

    assert any("caught stealing" in line.lower() for line in cleaned)

    assert any("wild pitch" in line.lower() for line in cleaned)

    assert any("passed ball" in line.lower() for line in cleaned)