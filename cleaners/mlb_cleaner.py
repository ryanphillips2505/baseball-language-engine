from __future__ import annotations

import re


_BASEBALL_ACTION_RE = re.compile(
    r"\b("
    r"singles|doubles|triples|homers|"
    r"walks|intentionally walks|"
    r"strikes out|called out on strikes|strikes out on a foul tip|"
    r"hit by pitch|"
    r"grounds out|grounds into|"
    r"flies out|lines out|pops out|"
    r"reaches on|"
    r"out on a sacrifice fly|"
    r"wild pitch by pitcher|passed ball by catcher|balk by pitcher|throwing error by|"
    r"starts inning at 2nd base|"
    r"steals|caught stealing|picked off"
    r")\b",
    re.I,
)

# MLB highlight captions:
# "Sonny Gray strikes out Brandon Nimmo"
# "Jack Leiter strikes out Jarren Duran"
_HIGHLIGHT_CAPTION_RE = re.compile(
    r"^[A-Z][A-Za-z'.-]+(?:\s+[A-Z][A-Za-z'.-]+)+\s+strikes out\s+"
    r"[A-Z][A-Za-z'.-]+(?:\s+[A-Z][A-Za-z'.-]+)*$",
    re.I,
)

# Standalone labels that appear above the real play description.
_STANDALONE_LABELS = {
    "single",
    "double",
    "triple",
    "home run",
    "walk",
    "strikeout",
    "flyout",
    "groundout",
    "lineout",
    "pop out",
    "hit by pitch",
    "sac fly",
}


def clean_mlb_text(raw_text: str) -> list[str]:
    cleaned_blocks: list[str] = []

    for raw_line in raw_text.splitlines():
        line = raw_line.strip()

        if not line:
            continue

        line = re.sub(r"\s+", " ", line)

        # Must contain baseball action language
        if not _BASEBALL_ACTION_RE.search(line):
            continue

        # Reject MLB video captions
        if _HIGHLIGHT_CAPTION_RE.match(line):
            continue

        # Reject standalone event labels
        if line.lower() in _STANDALONE_LABELS:
            continue

        cleaned_blocks.append(line)

    return cleaned_blocks