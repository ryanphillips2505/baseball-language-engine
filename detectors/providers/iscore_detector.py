import re

from detectors.source_detector import SourceType


def detect_iscore(text: str) -> SourceType | None:
    if "iscoresports.com" in text:
        return SourceType.ISCORE

    if re.search(r"\(\d+\)\s+#\d+", text):
        return SourceType.ISCORE

    return None