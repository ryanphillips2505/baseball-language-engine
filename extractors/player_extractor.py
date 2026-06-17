from __future__ import annotations


def extract_batter_name(pa_block: str) -> str | None:
    text = pa_block.strip()

    if not text:
        return None

    action_words = [
        " singled",
        " doubled",
        " tripled",
        " homered",
        " walked",
        " hit by pitch",
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
        " hits a ground ball",
        " hits a fly ball",
        " hits a line drive",
        " hits a pop fly",
        " hits a popup",
        " hits a bunt",
        " out on infield fly",
        " reaches",
       
    ]

    lowered = text.lower()

    for action in action_words:
        index = lowered.find(action)
        if index != -1:
            return text[:index].strip()

    return None