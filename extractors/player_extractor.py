from __future__ import annotations

import re


_PITCH_TOKEN_RE = re.compile(
    r"\b("
    r"Ball\s*\d+|"
    r"Strike\s*\d+\s*(?:looking|swinging)?|"
    r"Foul|"
    r"In play"
    r")\b",
    re.I,
)

_RUNNER_ONLY_ACTION_RE = re.compile(
    r"\b("
    r"steals|stole|caught stealing"
    r")\b",
    re.I,
)

# MLB challenge / umpire-review wrappers put review context before the final call.
# Examples:
# Shea Langeliers challenged (pitch result), call on the field was
# overturned: Nolan Schanuel called out on strikes.
# Umpire reviewed (home run), call on the field was upheld:
# Junior Caminero flies out sharply to center fielder Cam Cauley.
_CHALLENGE_FINAL_CALL_RE = re.compile(
    r"(?:challenged|umpire reviewed)\s*\([^)]*\)\s*,\s*call on the field was "
    r"(?:overturned|confirmed|upheld):\s*(.+)$",
    re.I,
)

# Pitcher-subject intentional walk: "Marco Gonzales intentionally walks Junior Caminero."
_INTENTIONAL_WALK_BATTER_RE = re.compile(
    r"\bintentionally walks\s+([^./]+?)(?:\.|$)",
    re.I,
)

# Batter-subject intentional walk: "John Smith is intentionally walked."
_IS_INTENTIONALLY_WALKED_RE = re.compile(
    r"^(.+?)\s+is intentionally walked\b",
    re.I,
)


def _looks_like_pitch_sequence_runner_line(text: str) -> bool:
    """
    GameChanger sometimes emits runner events inside pitch-sequence text.

    Examples:
    Strike 1 swinging, Zayden Khalil steals 2nd, Foul, Ball 1.
    Ball 1, Eddie Fish caught stealing home, catcher Cooper Cunningham.

    These lines can contain real runner events, but they should not create
    a batter name.
    """

    return bool(
        _PITCH_TOKEN_RE.search(text)
        and _RUNNER_ONLY_ACTION_RE.search(text)
    )


def extract_batter_name(pa_block: str) -> str | None:
    text = pa_block.strip()

    if not text:
        return None

    if _looks_like_pitch_sequence_runner_line(text):
        return None

    challenge_match = _CHALLENGE_FINAL_CALL_RE.search(text)
    if challenge_match:
        text = challenge_match.group(1).strip()

    # Intentional walks must not treat the pitcher as the batter.
    intentional_batter = _INTENTIONAL_WALK_BATTER_RE.search(text)
    if intentional_batter:
        return intentional_batter.group(1).strip()

    is_intentionally_walked = _IS_INTENTIONALLY_WALKED_RE.search(text)
    if is_intentionally_walked:
        return is_intentionally_walked.group(1).strip()

    action_words = [
        " pops into",
        " hits an inside the park home run",
        " hits a ground-rule double",
        " hits a hard ground ball",
        " hits a hard fly ball",
        " hits a hard line drive",
        " hits a hard pop fly",
        " hits a ground ball",
        " hits a fly ball",
        " hits a line drive",
        " lines into",
        " hits a pop fly",
        " hits a popup",
        " hits a sacrifice fly and",
        " hits a sacrifice fly",
        " hit sacrifice fly",
        " hits a sacrifice bunt",
        " hit sacrifice bunt",
        " hits a bunt",
        " bunts out",
        " bunts into",
        " bunts and",
        " is out on foul tip",
        " out on a sacrifice fly",
        " out on sacrifice fly",
        " called out on strikes",
        " sacrifices",
        " out on infield fly",
        " out at first on dropped 3rd strike",
        " out at first on dropped third strike",
        " is hit by pitch",
        " hit by pitch",
        " singled",
        " doubled",
        " tripled",
        " homered",
        " walked",
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
        " called out on strikes",
        " strikes out",
        " grounds",
        " flies",
        " lines",
        " pops",
        " reaches",
    ]

    lowered = text.lower()

    for action in action_words:
        index = lowered.find(action)
        if index != -1:
            return text[:index].strip()

    return None



