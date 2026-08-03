from __future__ import annotations

import re


_BASEBALL_ACTION_RE = re.compile(
    r"\b("
    r"singles|doubles|triples|homers|"
    r"hits a ground-rule double|ground-rule double|"
    r"walks|intentionally walks|"
    r"strikes out|called out on strikes|strikes out on a foul tip|"
    r"hit by pitch|"
    r"grounds out|grounds into|"
    r"flies out|lines out|lines into|pops out|pops into|"
    r"reaches on|"
    r"out on a sacrifice fly|out on a sacrifice bunt|"
    r"hits a sacrifice bunt|sacrifice bunt|"
    r"wild pitch by pitcher|passed ball by catcher|balk by pitcher|defensive indifference|throwing error by|"
    r"starts inning at 2nd base|"
    r"steals|caught stealing|picked off|picks off"
    r")\b",
    re.I,
)

# MLB highlight captions:
# "Sonny Gray strikes out Brandon Nimmo"
# "Jack Leiter strikes out Jarren Duran"
#
# The batter token after "strikes out" must start with a real capital letter.
# With a fully case-insensitive pattern, "strikes out swinging." was falsely
# rejected as a caption because "swinging" matched the batter-name group.
_HIGHLIGHT_CAPTION_RE = re.compile(
    r"^[A-Z][A-Za-z'.-]+(?:\s+[A-Z][A-Za-z'.-]+)+\s+strikes out\s+"
    r"(?-i:[A-Z])[A-Za-z'.-]+(?:\s+(?-i:[A-Z])[A-Za-z'.-]+)*\.?$",
    re.I,
)

# Standalone labels that appear above the real play description.
# Includes IQ Capture / Gameday summary chip labels.
_STANDALONE_LABELS = {
    "single",
    "double",
    "triple",
    "home run",
    "walk",
    "intent walk",
    "strikeout",
    "flyout",
    "groundout",
    "lineout",
    "pop out",
    "forceout",
    "hit by pitch",
    "sac fly",
    "sac bunt",
    "field error",
    "grounded into dp",
    "wild pitch",
    "passed ball",
    "defensive indiff",
}

# Video/recap captions that repeat a result already captured on the play line.
# Examples:
# "Colby Thomas strikes out after ABS challenge"
# "Ben Malgeri walks after ABS Challenge"
# "Gage Jump K's Dillon Dingler after ABS"
_ABS_RESULT_CAPTION_RE = re.compile(
    r"^.+\b(?:strikes out|called out on strikes|walks|K['’]?s)\b.+\bafter ABS\b",
    re.I,
)

# IQ Capture / Gameday highlight blurbs that reuse action verbs but are not
# official play descriptions.
# Example: "Freddie Freeman singles to extend hitting streak"
# Example: "Enmanuel De Jesus strikes out Henry Bolte to end game"
_HIGHLIGHT_NARRATIVE_RE = re.compile(
    r"\b("
    r"extend(?:s|ed|ing)?\s+hitting\s+streak|"
    r"hitting\s+streak|"
    r"solo\s+homer|"
    r"complete\s+sweep|"
    r"drives?\s+in\b|"
    r"makes\s+(?:a\s+)?(?:slick|diving)\b|"
    r"with\s+.+\s+bat\b|"
    r"to end(?:s|ed|ing)?(?:\s+the)?\s+game|"
    r"nifty play|"
    r"smooth diving"
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

        # Must contain baseball action language
        if not _BASEBALL_ACTION_RE.search(line):
            continue

        # Reject MLB video captions
        if _HIGHLIGHT_CAPTION_RE.match(line):
            continue

        if _ABS_RESULT_CAPTION_RE.match(line):
            continue

        if _HIGHLIGHT_NARRATIVE_RE.search(line):
            continue

        # Reject standalone event labels
        if line.lower() in _STANDALONE_LABELS:
            continue

        cleaned_blocks.append(line)

    return cleaned_blocks