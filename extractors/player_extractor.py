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
    ]

    lowered = text.lower()

    for action in action_words:
        index = lowered.find(action)
        if index != -1:
            return text[:index].strip()

    return None
