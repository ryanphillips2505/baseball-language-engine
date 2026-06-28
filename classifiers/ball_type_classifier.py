from __future__ import annotations


def classify_ball_type(pa_block: str) -> str | None:
    text = pa_block.lower()

    #
    # BUNTS
    #

    if "bunt" in text:
        return "BUNT"

    #
    # GROUND BALLS
    #

    if "ground ball" in text:
        return "GB"

    if "grounds out" in text:
        return "GB"

    if "grounded out" in text:
        return "GB"

    if "grounds into" in text:
        return "GB"

    if "grounded into" in text:
        return "GB"

    #
    # FLY BALLS
    #

    if "sacrifice fly" in text:
        return "FB"

    if "sac fly" in text:
        return "FB"

    if "fly ball" in text:
        return "FB"

    if "flies out" in text:
        return "FB"

    if "flied out" in text:
        return "FB"

    if "line drive" in text:
        return "FB"

    if "lines out" in text:
        return "FB"

    if "lines into" in text:
        return "FB"

    if "pops out" in text:
        return "FB"

    if "popped out" in text:
        return "FB"

    if "pop fly" in text:
        return "FB"

    if "infield fly" in text:
        return "FB"

    return None