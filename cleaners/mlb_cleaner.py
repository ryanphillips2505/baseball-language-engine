from __future__ import annotations

import re


_BASEBALL_ACTION_RE = re.compile(
    r"\b("
    r"singles|doubles|triples|homers|"
    r"walks|intentionally walks|"
    r"strikes out|called out on strikes|"
    r"hit by pitch|"
    r"grounds out|grounds into|"
    r"flies out|lines out|pops out|"
    r"reaches on|"
    r"out on a sacrifice fly|"
    r"steals|caught stealing|picked off"
    r")\b",
    re.I,
)


def clean_mlb_text(raw_text: str) -> list[str]:
    cleaned_blocks: list[str] = []

    for raw_line in raw_text.splitlines():
        line = raw_line.strip()

        if not line:
            continue

        line = re.sub(r"\s+", " ", line)

        if _BASEBALL_ACTION_RE.search(line):
            cleaned_blocks.append(line)

    return cleaned_blocks
