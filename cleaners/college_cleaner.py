from __future__ import annotations

import re


_COLLEGE_ACTION_RE = re.compile(
    r"\b("
    r"singled|doubled|tripled|homered|"
    r"walked|hit by pitch|"
    r"struck out|"
    r"grounded out|grounded into|"
    r"flied out|popped out|fouled out|lined out|"
    r"reached on|reached on infield single|"
    r"stole|caught stealing"
    r")\b",
    re.I,
)


def clean_college_text(raw_text: str) -> list[str]:
    cleaned_blocks: list[str] = []

    for raw_line in raw_text.splitlines():
        line = raw_line.strip()

        if not line:
            continue

        line = re.sub(r"\s+", " ", line)

        if _COLLEGE_ACTION_RE.search(line):
            cleaned_blocks.append(line)

    return cleaned_blocks
