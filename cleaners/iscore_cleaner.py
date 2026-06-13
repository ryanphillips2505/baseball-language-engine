from __future__ import annotations

import re


_ISCORE_ACTION_RE = re.compile(
    r"#\d+\s+.+?\b("
    r"hits|strikes out|is walked|is hit by the pitch|"
    r"reaches base|grounds out|flies out|"
    r"bunts|steals|is caught stealing|"
    r"is out on an infield fly rule"
    r")\b",
    re.I,
)


def clean_iscore_text(raw_text: str) -> list[str]:
    cleaned_blocks: list[str] = []

    for raw_line in raw_text.splitlines():
        line = raw_line.strip()

        if not line:
            continue

        line = re.sub(r"\s+", " ", line)

        if _ISCORE_ACTION_RE.search(line):
            cleaned_blocks.append(line)

    return cleaned_blocks