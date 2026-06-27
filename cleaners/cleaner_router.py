from cleaners.gamechanger_cleaner import clean_gamechanger_text
from cleaners.iscore_cleaner import clean_iscore_text
from cleaners.mlb_cleaner import clean_mlb_text
from cleaners.college_cleaner import clean_college_text
from detectors.source_detector import SourceType, detect_source


class UnsupportedSourceError(ValueError):
    pass


def clean_by_source(raw_text: str) -> list[str]:
    source = detect_source(raw_text)

    if source == SourceType.GAMECHANGER:
        return clean_gamechanger_text(raw_text)

    if source == SourceType.ISCORE:
        return clean_iscore_text(raw_text)

    if source == SourceType.MLB:
        return clean_mlb_text(raw_text)

    if source == SourceType.COLLEGE:
        return clean_college_text(raw_text)

    raise UnsupportedSourceError("Could not detect supported baseball data source.")
