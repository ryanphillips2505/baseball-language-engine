import pytest

from cleaners.cleaner_router import UnsupportedSourceError, clean_by_source


def test_clean_by_source_rejects_unknown_text():
    with pytest.raises(UnsupportedSourceError):
        clean_by_source("this is not baseball play by play text")


def test_clean_by_source_routes_gamechanger_text():
    raw_text = """
    All Plays
    Top 1st
    Strike 1 looking.
    Ball 1.
    In play.
    John Smith singles on a line drive to center fielder.
    """

    cleaned = clean_by_source(raw_text)

    assert isinstance(cleaned, list)