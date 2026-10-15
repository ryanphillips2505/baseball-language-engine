from __future__ import annotations

import re


# Lines that carry an iScore batter or runner result. iScore names carry a
# jersey prefix ("#12 John Smith", "#0 Ryan 6").
_ISCORE_ACTION_RE = re.compile(
    r"#\d+\s+.+?\b("
    r"hits|strikes out|is walked|is intentionally walked|is hit by the pitch|"
    r"is hit by the ball|is picked off|"
    r"reaches base|grounds out|grounds into|flies out|pops out|lines out|hits into|"
    r"bunts|steals|stole|is caught stealing|"
    r"is out on an infield fly rule|"
    r"homers|homerun|doubles|triples|singles"
    r")\b",
    re.I,
)

# iScore often prefixes the result with the final pitch on the same line:
# "Strike 3. #0 Ryan 2 strikes out swinging."
_LEADING_PITCH_TOKEN_RE = re.compile(
    r"^(?:(?:Ball|Strike)\s*\d+\.\s*|Foul Ball\.\s*)+",
    re.I,
)

_TRAILING_NOISE_RE = re.compile(r"\s*(?:Game Over\.?)\s*$", re.I)

# iScore wording rewritten into phrases BLE's readers already know.
_ISCORE_REWRITES: list[tuple[re.Pattern, str]] = [
    (re.compile(r"\bhits a ground rule double\b", re.I), "hits a ground-rule double"),
    (re.compile(r"\bhits a (?:hard|medium|soft) line drive\b", re.I), "hits a line drive"),
    (re.compile(r"\bhits a (?:hard|medium|soft) fly ball\b", re.I), "hits a fly ball"),
    (re.compile(r"\bhits a (?:hard|medium|soft) ground ball\b", re.I), "hits a ground ball"),
    # A dropped third strike on a wild pitch / passed ball is a strikeout.
    (
        re.compile(r"\breaches base due to a (wild pitch|passed ball) third strike\b", re.I),
        r"strikes out, reaches first on a \1",
    ),
]


def _normalize_iscore_action_line(line: str) -> str:
    """
    iScore export quirks rewritten into phrases BLE already reads.

    Applied only to text detected as iScore; GameChanger text never passes
    through this cleaner.
    """
    cleaned = re.sub(r"\s+", " ", (line or "").strip())
    if not cleaned:
        return ""

    cleaned = _LEADING_PITCH_TOKEN_RE.sub("", cleaned).strip()
    cleaned = _TRAILING_NOISE_RE.sub("", cleaned).strip()

    for pattern, replacement in _ISCORE_REWRITES:
        cleaned = pattern.sub(replacement, cleaned)

    return cleaned.strip()


def clean_iscore_text(raw_text: str) -> list[str]:
    cleaned_blocks: list[str] = []

    for raw_line in str(raw_text or "").splitlines():
        line = _normalize_iscore_action_line(raw_line)

        if not line:
            continue

        if _ISCORE_ACTION_RE.search(line):
            cleaned_blocks.append(line)

    return cleaned_blocks
