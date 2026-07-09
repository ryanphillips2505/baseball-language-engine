from __future__ import annotations

import re
from difflib import SequenceMatcher


# Lines that are clearly GameChanger page chrome / footer noise and should never
# reach the parser.
_NOISE_PATTERNS = [
    r"^Get the App$",
    r"^Privacy$",
    r"^Terms$",
    r"^Support$",
    r"^Home$",
    r"^Info$",
    r"^Videos$",
    r"^Recap$",
    r"^Box Score$",
    r"^Plays$",
    r"^All Plays$",
    r"^Scoring Plays$",
    r"^Outs$",
    r"^Player$",
    r"^Reverse Chronological$",
    r"^Try our Family Plan$",
    r"^GameChanger is a proud member.*$",
    r"^\(Play Edit\)$",
    r"^Play Edit$",
    r"^Status$",
    r"^CA Disclosures$",
    r"^Your Privacy Choices$",
    r"^All rights reserved.*$",
    r"^©\s*GameChanger Media, Inc\..*$",
]

_NOISE_RE = re.compile("|".join(f"(?:{p})" for p in _NOISE_PATTERNS), flags=re.I)

# Prefixes that often appear inside real baseball lines.
_LINEUP_CHANGE_RE = re.compile(r"^Lineup\s+changed:\s*", re.I)
_SUBSTITUTION_RE = re.compile(
    r"^(Substitution:|Pinch runner:|Pinch hitter:|Courtesy runner:)\s*",
    re.I,
)

# Scoreboard / page chrome patterns seen in pasted GC text.
_TEAM_CODE_ROW_RE = re.compile(r"^[A-Z0-9]{2,8}\s+[A-Z0-9]{2,8}$")
_INNING_NUMBERS_ROW_RE = re.compile(r"^\d+(?:\s+\d+){6,}$")
_RHE_ROW_RE = re.compile(r"^R\s+H\s+E$", re.I)
_RHE_COMPACT_RE = re.compile(r"^RHE$", re.I)
_TEAM_SCORE_LINE_RE = re.compile(r"^[A-Z0-9]{2,8}\s+\d+\s*-\s*[A-Z0-9]{2,8}\s+\d+$", re.I)
_PURE_SCORE_ROW_RE = re.compile(r"^\d+(?:\s+\d+){1,}$")
_TIME_RE = re.compile(r"^\d{1,2}:\d{2}\s?(AM|PM)\b", re.I)
_DATEISH_RE = re.compile(
    r"\b(Mon|Tue|Tues|Wed|Thu|Thur|Fri|Sat|Sun)\b.*\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)\b",
    re.I,
)
_INNING_HEADER_RE = re.compile(r"^(Top|Bottom)\s+\d+(st|nd|rd|th)?\b", re.I)
_OUTS_HEADER_RE = re.compile(r"^\d+\s+Outs?$", re.I)
_FINAL_RE = re.compile(r"^Final$", re.I)
_BACK_TO_SCHEDULE_RE = re.compile(r"^Back to Schedule$", re.I)
_LOGO_RE = re.compile(r".+\s+logo(?:\s+live)?$", re.I)
_GET_APP_PROMO_RE = re.compile(r"^Try our Family Plan$", re.I)

# Team names / page labels that often leak in as standalone junk lines.
_STANDALONE_UI_LABEL_RE = re.compile(
    r"^(Home|Away|live|Recap|Box Score|Plays|Videos|Info)$",
    re.I,
)

# Raw-text opponent extraction helpers.
_INNING_TEAM_CAPTURE_RE = re.compile(
    r"^(Top|Bottom)\s+\d+(?:st|nd|rd|th)?\s*-\s*(.+?)\s*$",
    re.I,
)
_VS_LINE_RE = re.compile(
    r"^\s*(.+?)\s+vs\.?\s+(.+?)\s*$",
    re.I,
)

# Baseball-content detectors so mixed GC lines survive normalization.
_PITCH_TOKEN_RE = re.compile(
    r"(Ball\s*\d+|"
    r"Strike\s*\d+\s*(?:looking|swinging)?|"
    r"Called Strike|"
    r"Swinging Strike|"
    r"Strike Looking|"
    r"Foul tip|"
    r"Foul bunt|"
    r"Bunt foul|"
    r"Foul|"
    r"In play|"
    r"Pickoff attempt at (?:1st|2nd|3rd))",
    re.I,
)

_BASEBALL_ACTION_RE = re.compile(
    r"\b("
    r"strikes out|walks|intentionally walks|hit by pitch|"
    r"singles|doubles|triples|homers|hits a home run|"
    r"grounds out|grounds into|flies out|flies into|"
    r"lines out|lines into|pops out|"
    r"bunt single|singles on a bunt|on a bunt|"
    r"bunts out|bunts into|bunts to|bunts toward|bunts down|"
    r"squares to bunt|"
    r"reaches on error|reaches on an error|"
    r"reaches on a dropped 3rd strike|reaches on dropped 3rd strike|"
    r"out on sacrifice fly|out on sacrifice bunt|"
    r"sacrifice fly|sacrifice bunt|sacrifices|"
    r"fielder'?s choice|double play|triple play|"
    r"out at first|out at second|out at third|out at home|"
    r"caught stealing|picked off|steals|stole|"
    r"advances to|advances on|scores|remains at|"
    r"is hit by pitch|is out on foul tip"
    r")\b",
    re.I,
)


def split_lines(text: str) -> list[str]:
    lines = []
    for raw in text.splitlines():
        l = raw.strip()
        if not l:
            continue
        cleaned = clean_gc_line(l)
        if not cleaned:
            continue
        lines.append(cleaned)
    return lines


def _has_baseball_content(line: str) -> bool:
    line = str(line or "").strip()
    if not line:
        return False
    return bool(_PITCH_TOKEN_RE.search(line) or _BASEBALL_ACTION_RE.search(line))


def is_gc_noise_line(line: str) -> bool:
    line = line.strip()
    if not line:
        return True

    normalized = re.sub(r"\s+", " ", line).strip()

    if _NOISE_RE.match(normalized):
        return True

    # IMPORTANT:
    # Do NOT treat lineup/substitution prefixes as automatic noise.
    # GC often puts real pitch/action content on those same lines.
    # Example:
    # "Lineup changed: K Hotz in for batter O Blair, Ball 1, Strike 1 looking, Ball 2..."
    if _LINEUP_CHANGE_RE.match(normalized) or _SUBSTITUTION_RE.match(normalized):
        return not _has_baseball_content(normalized)

    # Keep inning headers. They are useful for downstream parsing and opponent detection.
    if _INNING_HEADER_RE.match(normalized):
        return False

    # Outs lines are meaningful structure for the parser.
    if _OUTS_HEADER_RE.match(normalized):
        return False

    if _TEAM_CODE_ROW_RE.match(normalized):
        return True

    if _INNING_NUMBERS_ROW_RE.match(normalized):
        return True

    compact = normalized.replace("\t", " ")
    compact = re.sub(r"\s+", " ", compact).strip()

    if _RHE_ROW_RE.match(compact):
        return True

    if _RHE_COMPACT_RE.match(compact.replace(" ", "")):
        return True

    if _TEAM_SCORE_LINE_RE.match(compact):
        return True

    if _TIME_RE.match(normalized):
        return True

    if _DATEISH_RE.search(normalized):
        return True

    if _FINAL_RE.match(normalized):
        return True

    if _BACK_TO_SCHEDULE_RE.match(normalized):
        return True

    if _LOGO_RE.match(normalized):
        return True

    if _GET_APP_PROMO_RE.match(normalized):
        return True

    if _STANDALONE_UI_LABEL_RE.match(normalized):
        return True

    if "gamechanger media, inc." in normalized.lower():
        return True

    if "all rights reserved" in normalized.lower():
        return True

    if _TEAM_SCORE_LINE_RE.match(normalized):
        return True

    if _PURE_SCORE_ROW_RE.match(normalized):
        parts = normalized.split()
        if len(parts) >= 2:
            return True

    return False


def clean_gc_line(line: str) -> str:
    """
    Normalize a single GameChanger line without destroying baseball meaning.

    Critical rules:
    - Do NOT strip words like "strike" globally.
    - Do NOT discard lineup/substitution lines if they also contain baseball content.
    - Keep inning headers and outs headers.
    """
    line = line.strip()
    if not line:
        return ""

    line = (
        line.replace("\u2019", "'")
        .replace("\u2018", "'")
        .replace("\u201c", '"')
        .replace("\u201d", '"')
        .replace("\xa0", " ")
    )
    line = re.sub(r"\s+", " ", line).strip()

    if is_gc_noise_line(line):
        return ""

    line = re.sub(r"[|]{2,}", "|", line)
    line = re.sub(r"[-]{3,}", "-", line)

    if re.fullmatch(r"\(?\s*Play Edit\s*\)?", line, flags=re.I):
        return ""

    # IMPORTANT:
    # Do not strip lineup/substitution prefixes anymore.
    # They may carry real pitch tokens and action text on the same line.
    # Keep them intact so downstream token extraction can still see:
    # "Ball 1, Strike 1 looking, Ball 2..."
    if not line:
        return ""

    if is_gc_noise_line(line):
        return ""

    return line


def _expand_gc_compound_line(line: str) -> list[str]:
    """
    Additive hardening only.

    Normalize both GC copy styles to the same internal line shape.

    Examples:
      Ground Out|3 Outs           -> ["Ground Out", "3 Outs"]
      Walk|JNKS 1 - BXBY 0        -> ["Walk", "JNKS 1 - BXBY 0"]
      Single|JNKS 5 - BXBY 1 | 2 Outs
                                  -> ["Single", "JNKS 5 - BXBY 1", "2 Outs"]

    Lines that are already split stay unchanged.
    """
    line = str(line or "").strip()
    if not line:
        return []

    if "|" not in line:
        return [line]

    parts = [p.strip() for p in line.split("|") if p.strip()]
    if not parts:
        return []

    return parts


def normalize_pbp(text: str) -> list[str]:
    lines = []

    for raw in text.splitlines():
        cleaned = clean_gc_line(raw)
        if not cleaned:
            continue

        expanded_lines = _expand_gc_compound_line(cleaned)

        for expanded in expanded_lines:
            if expanded:
                lines.append(expanded)

    return lines


def _normalize_team_name(name: str) -> str:
    name = (name or "").strip()
    if not name:
        return ""

    name = (
        name.replace("\u2019", "'")
        .replace("\u2018", "'")
        .replace("\u201c", '"')
        .replace("\u201d", '"')
        .replace("\xa0", " ")
    )
    name = re.sub(r"\s+", " ", name).strip()

    name = re.sub(r"\s+(logo(?:\s+live)?)$", "", name, flags=re.I).strip()
    name = re.sub(r"\s+(live)$", "", name, flags=re.I).strip()

    return name


def _team_key(name: str) -> str:
    """
    Aggressive normalization for fuzzy team comparison.
    """
    name = _normalize_team_name(name).lower()
    if not name:
        return ""

    name = re.sub(r"[^a-z0-9\s]", " ", name)
    name = re.sub(r"\s+", " ", name).strip()

    stop_words = {
        "varsity",
        "junior",
        "jv",
        "freshman",
        "baseball",
        "high",
        "school",
        "hs",
        "team",
        "club",
        "millers",
        "tigers",
        "lions",
        "huskies",
        "patriots",
        "bulldogs",
        "wolves",
        "wildcats",
        "eagles",
        "sooners",
        "trojans",
        "panthers",
        "bears",
        "pirates",
        "chargers",
        "mustangs",
        "bronchos",
        "broncos",
    }
    tokens = [t for t in name.split() if t not in stop_words]
    return " ".join(tokens).strip()


def _similarity(a: str, b: str) -> float:
    a_key = _team_key(a)
    b_key = _team_key(b)

    if not a_key or not b_key:
        return 0.0

    if a_key == b_key:
        return 1.0

    if a_key in b_key or b_key in a_key:
        return 0.95

    a_tokens = set(a_key.split())
    b_tokens = set(b_key.split())
    if a_tokens and b_tokens:
        overlap = len(a_tokens & b_tokens) / max(len(a_tokens), len(b_tokens))
    else:
        overlap = 0.0

    ratio = SequenceMatcher(None, a_key, b_key).ratio()
    return max(ratio, overlap)


def _extract_team_names_from_inning_headers(text: str) -> list[str]:
    """
    Pull team names from raw lines like:
    Top 7th - Norman Tigers Varsity 26'
    Bottom 7th - Yukon Millers Varsity
    """
    found: list[str] = []
    seen: set[str] = set()

    for raw in text.splitlines():
        line = re.sub(r"\s+", " ", raw.strip())
        if not line:
            continue

        m = _INNING_TEAM_CAPTURE_RE.match(line)
        if not m:
            continue

        team_name = _normalize_team_name(m.group(2))
        if not team_name:
            continue

        key = team_name.casefold()
        if key not in seen:
            seen.add(key)
            found.append(team_name)

    return found


def guess_opponent_from_gc_text(text: str, selected_team_name: str | None = None) -> str | None:
    """
    Guess the opponent name from raw GameChanger pasted text.

    Priority:
    1. Inning headers like:
       Top 7th - Norman Tigers Varsity 26'
       Bottom 7th - Yukon Millers Varsity
    2. Fallback to a simple "X vs Y" line if present.

    If selected_team_name is provided, choose the extracted GC team name that is
    closest to it, then return the other team as the opponent.
    """
    team_names = _extract_team_names_from_inning_headers(text)

    if len(team_names) >= 2:
        if selected_team_name:
            best_idx = max(
                range(len(team_names)),
                key=lambda i: _similarity(selected_team_name, team_names[i]),
            )
            other_names = [name for i, name in enumerate(team_names) if i != best_idx]
            if other_names:
                return other_names[0]
        return team_names[0]

    if len(team_names) == 1:
        only_team = team_names[0]
        if selected_team_name and _similarity(selected_team_name, only_team) >= 0.6:
            return None
        return only_team

    raw_lines = [re.sub(r"\s+", " ", line.strip()) for line in text.splitlines() if line.strip()]
    for line in raw_lines:
        m = _VS_LINE_RE.match(line)
        if not m:
            continue

        left = _normalize_team_name(m.group(1))
        right = _normalize_team_name(m.group(2))

        if selected_team_name:
            left_score = _similarity(selected_team_name, left)
            right_score = _similarity(selected_team_name, right)

            if left_score >= right_score:
                return right or left
            return left or right

        if right:
            return right
        if left:
            return left
        
def clean_gamechanger_text(raw_text: str) -> list[str]:
    lines = normalize_pbp(raw_text)

    result_lines = []

    standalone_labels = {
        "single",
        "double",
        "triple",
        "home run",
        "walk",
        "strikeout",
        "fly out",
        "flyout",
        "ground out",
        "groundout",
        "line out",
        "lineout",
        "pop out",
        "error",
        "hit by pitch",
        "fielder's choice",
        "double play",
        "sacrifice fly",
        "sacrifice bunt",
    }

    for line in lines:
        if line.lower() in standalone_labels:
            continue

        # Reject pitch-sequence/support lines that don't contain
        # an actual batter result.
        if _PITCH_TOKEN_RE.search(line) and not any(
            phrase in line.lower()
            for phrase in (
                "strikes out",
                "is out on foul tip",
                "walks",
                "singles",
                "doubles",
                "triples",
                "homers",
                "grounds out",
                "flies out",
                "lines out",
                "pops out",
                "hit by pitch",
                "fielder's choice",
                "reaches on",
                "bunt",
                "bunts",
                "sacrifice bunt",
                "sacrifices",
                "squares to bunt",
                "steals",
                "stole",
                "caught stealing",
            )
        ):
            continue

        if _BASEBALL_ACTION_RE.search(line):
            result_lines.append(line)

    return result_lines