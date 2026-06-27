from __future__ import annotations


def classify_location(pa_block: str) -> str | None:
    text = pa_block.lower()

    # Outfield direction
    if "left-center" in text or "left center" in text or " lcf" in text:
        return "LF"

    if "right-center" in text or "right center" in text or " rcf" in text:
        return "RF"

    if "to left" in text:
        return "LF"

    if "to center" in text:
        return "CF"

    if "to right" in text:
        return "RF"

    # GameChanger infield fielder phrases.
    # Check these before "to first" so throws to first do not become location 1B.
    if "third baseman" in text:
        return "3B"

    if "shortstop" in text:
        return "SS"

    if "second baseman" in text:
        return "2B"

    if "first baseman" in text:
        return "1B"

    if "pitcher" in text:
        return "P"

    if "catcher" in text:
        return "C"

    # Generic fallback
    if "to third" in text:
        return "3B"

    if "to shortstop" in text:
        return "SS"

    if "to second" in text:
        return "2B"

    if "to first" in text:
        return "1B"

    if "to catcher" in text:
        return "C"

    if "to pitcher" in text:
        return "P"

    return None