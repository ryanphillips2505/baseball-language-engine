from __future__ import annotations


def classify_location(pa_block: str) -> str | None:
    text = pa_block.lower()

    #
    # OUTFIELD
    #

    if "to left" in text:
        return "LF"

    if "to center" in text:
        return "CF"

    if "to right" in text:
        return "RF"

    #
    # INFIELD
    #

    if "to third" in text:
        return "3B"

    if "to shortstop" in text:
        return "SS"

    if "to second" in text:
        return "2B"

    if "to first" in text:
        return "1B"

    if "to pitcher" in text:
        return "P"

    return None