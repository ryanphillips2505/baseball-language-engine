from __future__ import annotations

import re

from language.pages import extract_statcrew_plays


_COLLEGE_ACTION_RE = re.compile(
    r"\b("
    r"singled|doubled|tripled|homered|"
    r"walked|hit by pitch|"
    r"hit sacrifice fly|hit sacrifice bunt|"
    # SIDEARM bare forms: "Castro sacrifice fly to rf", "Wallace sacrifice
    # bunt to first base", "Castro flew into double play to rf".
    r"sacrifice fly|sacrifice bunt|flew into|flew out|"
    r"wild pitch|passed ball|"
    r"struck out|strikes out|"
    r"grounded out|grounded into|"
    r"flied out|popped out|fouled out|lined out|"
    r"popped up|lined into|flied into|popped into|hit into|"
    r"hit a ground[- ]rule double|ground[- ]rule|"
    r"out at first|safe at first|safe at second|safe at third|sacrificed|sacrified|"
    r"reached on|reached on infield single|reached on bunt single|bunt single|"
    r"intentionally walked|picked off|infield fly|"
    # ESPN sometimes glues the base on: "caught stealingsecond".
    r"stole|caught stealing|caught stealing(?:second|third|home)|"
    # Present tense: college scorecards imported from GameChanger-style
    # scoring ("DeVault walks, Garza pitching").
    r"singles|doubles|triples|homers|walks|"
    r"grounds out|grounds into|flies out|flies into|lines out|lines into|"
    r"pops out|pops into|bunts|reaches|is hit by pitch|hits a|hits an|"
    r"out on a sacrifice|sacrifices|steals|picks off"
    r")\b",
    re.I,
)


def clean_college_text(raw_text: str) -> list[str]:
    cleaned_blocks: list[str] = []

    # Whole SIDEARM / Presto pages repeat plays (scoring summary, per-inning
    # tabs). Keep each half inning once; plain play-by-play is unchanged.
    raw_text = extract_statcrew_plays(raw_text)

    for raw_line in raw_text.splitlines():
        line = raw_line.strip()

        if not line:
            continue

        line = re.sub(r"\s+", " ", line)

        if _COLLEGE_ACTION_RE.search(line):
            cleaned_blocks.append(line)

    return cleaned_blocks