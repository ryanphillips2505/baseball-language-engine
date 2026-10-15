from __future__ import annotations

import re

from cleaners.mlb_cleaner import clean_mlb_text
from models.timeline_block import GameEventBlock, PlateAppearanceBlock, TimelineBlock


_CAUGHT_STEALING_RE = re.compile(
    r"\bcaught stealing\b",
    re.I,
)

_STOLEN_BASE_RE = re.compile(
    r"\bsteals\b",
    re.I,
)

_WILD_PITCH_RE = re.compile(
    r"\bwild pitch\b",
    re.I,
)

_PICKED_OFF_RE = re.compile(
    r"\bpicked off\b",
    re.I,
)

_PASSED_BALL_RE = re.compile(
    r"\bpassed ball\b",
    re.I,
)

_BALK_RE = re.compile(
    r"\bbalk\b",
    re.I,
)

_DEFENSIVE_INDIFFERENCE_RE = re.compile(
    r"\bdefensive indifference\b",
    re.I,
)


# "With Isiah Kiner-Falefa batting, Tommy Pham picked off ..."
_WITH_BATTING_PREFIX_RE = re.compile(r"^With [^,]+ batting,\s*")

# "Pirates challenged (tag play), call on the field was upheld: ..."
_REVIEW_PREFIX_RE = re.compile(
    r"^[^:]*\b(?:challenged|review(?:ed)?|overturned|confirmed|upheld|stands)\b[^:]*:\s*",
    re.I,
)

_STEAL_OR_CAUGHT_RE = re.compile(r"\b(?:steals|caught stealing)\b", re.I)

_SENTENCE_SPLIT_RE = re.compile(
    r"(?<=[a-z0-9)]{2})\.\s+(?=[A-Z])"
    # "X strikes out swinging and Y caught stealing 2nd"
    r"|,?\s+and\s+(?=(?:[A-Z][^\s,]*\s+){1,4}(?:caught stealing|steals|picked off))"
)

_BATTER_OUTCOME_RE = re.compile(
    r"\b(?:strikes out|called out on strikes|walks|intentionally walks|hit by pitch|"
    r"singles|doubles|triples|homers|hits a|hits an|grounds|flies|lines|pops|bunt|"
    r"reaches|out on a sacrifice|hit into|sacrifices)\b",
    re.I,
)

_RUNNER_ACTION_RE = re.compile(
    r"\b(?:steals|stole|caught stealing|picked off|wild pitch|passed ball|balk|"
    r"defensive indifference)\b",
    re.I,
)


def _split_batter_and_runner_actions(block: str) -> list[str]:
    """
    Gameday writes runner actions that happened during a plate
    appearance into the same description as its result:

        "Jackson Chourio strikes out swinging. Sal Frelick steals (14) 2nd base."
        "José Caballero walks. Chandler Simpson to 3rd. Wild pitch by pitcher X."

    The plate appearance and each runner action are returned as
    separate blocks so the batter's result is kept and the runner
    action is credited to the runner.
    """

    block = _REVIEW_PREFIX_RE.sub("", block)
    block = _WITH_BATTING_PREFIX_RE.sub("", block)
    sentences = [part.strip() for part in _SENTENCE_SPLIT_RE.split(block) if part and part.strip()]

    if len(sentences) < 2:
        return [block]

    first = sentences[0]

    # Double steal: "Lindor steals (23) 3rd base. Soto steals (21) 2nd base."
    # Each runner gets an event of his own.
    if _RUNNER_ACTION_RE.search(first):
        steals = [sentence for sentence in sentences if _STEAL_OR_CAUGHT_RE.search(sentence)]
        return steals if len(steals) > 1 and len(steals) == len(
            [sentence for sentence in sentences if _RUNNER_ACTION_RE.search(sentence)]
        ) else [block]

    if not _BATTER_OUTCOME_RE.search(first):
        return [block]

    runner_sentences = [sentence for sentence in sentences[1:] if _RUNNER_ACTION_RE.search(sentence)]

    if not runner_sentences:
        return [block]

    plate_appearance = ". ".join(
        sentence.rstrip(".") for sentence in sentences if sentence not in runner_sentences
    ) + "."

    return [plate_appearance, *runner_sentences]


def clean_mlb_timeline_text(raw_text: str) -> list[TimelineBlock]:

    cleaned = [
        part
        for block in clean_mlb_text(raw_text)
        for part in _split_batter_and_runner_actions(block)
    ]

    timeline_blocks: list[TimelineBlock] = []

    for block in cleaned:

        if _CAUGHT_STEALING_RE.search(block):
            timeline_blocks.append(
                GameEventBlock(
                    raw_text=block,
                    event_type="caught_stealing",
                    source="mlb",
                )
            )
            continue

        if _STOLEN_BASE_RE.search(block):
            timeline_blocks.append(
                GameEventBlock(
                    raw_text=block,
                    event_type="stolen_base",
                    source="mlb",
                )
            )
            continue

        if _WILD_PITCH_RE.search(block):
            timeline_blocks.append(
                GameEventBlock(
                    raw_text=block,
                    event_type="wild_pitch",
                    source="mlb",
                )
            )
            continue

        if _PICKED_OFF_RE.search(block):
            timeline_blocks.append(
                GameEventBlock(
                    raw_text=block,
                    event_type="pickoff",
                    source="mlb",
                )
            )
            continue

        if _PASSED_BALL_RE.search(block):
            timeline_blocks.append(
                GameEventBlock(
                    raw_text=block,
                    event_type="passed_ball",
                    source="mlb",
                )
            )
            continue

        if _BALK_RE.search(block):
            timeline_blocks.append(
                GameEventBlock(
                    raw_text=block,
                    event_type="balk",
                    source="mlb",
                )
            )
            continue

        if _DEFENSIVE_INDIFFERENCE_RE.search(block):
            timeline_blocks.append(
                GameEventBlock(
                    raw_text=block,
                    event_type="defensive_indifference",
                    source="mlb",
                )
            )
            continue

        timeline_blocks.append(
            PlateAppearanceBlock(
                raw_text=block,
                source="mlb",
            )
        )

    return timeline_blocks


__all__ = [
    "clean_mlb_timeline_text",
]
