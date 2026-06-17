from __future__ import annotations


def extract_batter_name(pa_block: str) -> str | None:
    text = pa_block.strip()

    if not text:
        return None

    action_words = [
        " hits a hard ground ball",
        " hits a hard fly ball",
        " hits a hard line drive",
        " hits a hard pop fly",
        " hits a ground ball",
        " hits a fly ball",
        " hits a line drive",
        " hits a pop fly",
        " hits a popup",
        " hits a bunt",
        " bunts and",
        " out on infield fly",
        " is hit by pitch",
        " hit by pitch",
        " singled",
        " doubled",
        " tripled",
        " homered",
        " walked",
        " struck out",
        " grounded",
        " flied",
        " lined",
        " popped",
        " fouled",
        " reached",
        " stole",
        " caught stealing",
        " singles",
        " doubles",
        " triples",
        " homers",
        " walks",
        " strikes out",
        " grounds",
        " flies",
        " lines",
        " pops",
        " reaches",
    ]

    lowered = text.lower()

    for action in action_words:
        index = lowered.find(action)
        if index != -1:
            return text[:index].strip()

    return None