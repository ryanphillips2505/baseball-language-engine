"""Ranked team names ("#1 Tennessee Wesleyan") on a whole college page
are not iScore jersey prefixes. Real iScore text stays iScore."""

from pathlib import Path

import pytest

from detectors.source_detector import (
    SourceType,
    detect_source,
    detect_source_with_language_fallbacks,
)
from language.pages import has_iscore_markers

ISCORE_SAMPLES = sorted(Path(__file__).resolve().parents[1].glob("samples/iscore/**/*.txt"))

RANKED_PRESTO_PAGE = """January 29, 2025 #24 British Columbia at #1 Tennessee Wesleyan
#24 British Columbia
#1 Tennessee Wesleyan
Play-by-Play
Top of 1st
Smith, J. struck out swinging.
(1 out)
Jones, K. singled to left field.
Lee, M. grounded out to ss.
(2 out)
Brown, T. flied out to cf.
(3 out)
Bottom of 1st
Gann, V. walked.
Fort, P. struck out looking.
(1 out)
Watts, P. doubled to left center.
Garcia, J. lined out to 2b.
(2 out)
DP:
Devin Dixon (2)
#17 Indiana Southeast
"""


def test_ranked_page_is_iscore_to_detect_source_but_college_after_fallbacks():
    # detect_source is what live routing calls; it is left unchanged.
    assert detect_source(RANKED_PRESTO_PAGE) == SourceType.ISCORE
    assert not has_iscore_markers(RANKED_PRESTO_PAGE)
    assert detect_source_with_language_fallbacks(RANKED_PRESTO_PAGE) == SourceType.COLLEGE


@pytest.mark.parametrize("path", ISCORE_SAMPLES, ids=lambda p: p.name)
def test_real_iscore_samples_stay_iscore(path):
    text = path.read_text(encoding="utf-8")
    assert detect_source_with_language_fallbacks(text) == SourceType.ISCORE


def test_iscore_batting_order_marker_on_one_line_is_real_iscore():
    assert has_iscore_markers("(3) #12 John Smith singles to left")
    assert has_iscore_markers("Box score from iscoresports.com")
    assert not has_iscore_markers("Devin Dixon (2)\n#17 Indiana Southeast")
