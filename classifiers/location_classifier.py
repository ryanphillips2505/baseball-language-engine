from __future__ import annotations


def classify_location(pa_block: str) -> str | None:
    text = pa_block.lower()

    if "bunts and reaches on an error by pitcher" in text:
        return "P"

    if "bunts and reaches on an error by the pitcher" in text:
        return "P"

    candidates: list[tuple[int, str]] = []

    def add_candidate(phrases: list[str], location: str) -> None:
        for phrase in phrases:
            index = text.find(phrase)
            if index != -1:
                candidates.append((index, location))

    add_candidate(
        [
            "left-center",
            "left center",
            " lcf",
            "to left fielder",
            "to left field",
            "to left",
            "left fielder",
        ],
        "LF",
    )

    add_candidate(
        [
            "right-center",
            "right center",
            " rcf",
            "to right fielder",
            "to right field",
            "to right",
            "right fielder",
        ],
        "RF",
    )

    add_candidate(
        [
            "to center fielder",
            "to center field",
            "to center",
            "center fielder",
        ],
        "CF",
    )

    add_candidate(
        [
            "third baseman",
            "to third baseman",
            "to third",
        ],
        "3B",
    )

    add_candidate(
        [
            "shortstop",
            "to shortstop",
        ],
        "SS",
    )

    add_candidate(
        [
            "second baseman",
            "to second baseman",
            "to second",
        ],
        "2B",
    )

    add_candidate(
        [
            "first baseman",
            "to first baseman",
            "to first",
        ],
        "1B",
    )

    # Do NOT use bare "pitcher".
    # GC often writes:
    # "grounds out, pitcher Name to second baseman..."
    # Legacy does not classify that as P unless there is an explicit pitcher-fielding phrase.
    add_candidate(
        [
            "to pitcher",
            "to the pitcher",
            "back to pitcher",
            "back to the pitcher",
            "back to the mound",
            "pitcher fields",
            "fielded by pitcher",
            "fielded by the pitcher",
            "pitcher to",
        ],
        "P",
    )

    add_candidate(
        [
            "catcher",
            "to catcher",
        ],
        "C",
    )

    if candidates:
        _, location = min(candidates, key=lambda item: item[0])
        return location

    return None