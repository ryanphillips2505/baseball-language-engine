from enum import Enum
from typing import Callable


class SourceType(str, Enum):
    GAMECHANGER = "gamechanger"
    ISCORE = "iscore"
    MLB = "mlb"
    COLLEGE = "college"
    UNKNOWN = "unknown"


SourceDetector = Callable[[str], SourceType | None]


def _get_detectors() -> list[SourceDetector]:
    from detectors.providers.college_detector import detect_college
    from detectors.providers.gamechanger_detector import detect_gamechanger
    from detectors.providers.iscore_detector import detect_iscore
    from detectors.providers.mlb_detector import detect_mlb

    return [
        detect_iscore,
        detect_gamechanger,
        detect_college,
        detect_mlb,
    ]


def detect_source(raw_text: str) -> SourceType:
    if not raw_text:
        return SourceType.UNKNOWN

    text = raw_text.lower()

    for detector in _get_detectors():
        source = detector(text)

        if source is not None:
            return source

    return SourceType.UNKNOWN


__all__ = [
    "SourceType",
    "SourceDetector",
    "detect_source",
]
