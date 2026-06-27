from __future__ import annotations

from collections.abc import Callable

from cleaners.college_cleaner import clean_college_text
from cleaners.gamechanger_cleaner import clean_gamechanger_text
from cleaners.iscore_cleaner import clean_iscore_text
from cleaners.mlb_cleaner import clean_mlb_text
from detectors.source_detector import SourceType, detect_source


class UnsupportedSourceError(ValueError):
    pass


Cleaner = Callable[[str], list[str]]


CLEANERS: dict[SourceType, Cleaner] = {
    SourceType.GAMECHANGER: clean_gamechanger_text,
    SourceType.ISCORE: clean_iscore_text,
    SourceType.MLB: clean_mlb_text,
    SourceType.COLLEGE: clean_college_text,
}


def clean_by_source(raw_text: str) -> list[str]:
    source = detect_source(raw_text)

    cleaner = CLEANERS.get(source)

    if cleaner is None:
        raise UnsupportedSourceError(
            f"No cleaner registered for source: {source.value}"
        )

    return cleaner(raw_text)


__all__ = [
    "clean_by_source",
    "UnsupportedSourceError",
    "CLEANERS",
]