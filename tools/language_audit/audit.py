"""
Run harvested play-by-play through BLE and report misreads by phrasing.

Each play is read the way the pipeline reads it: the platform's
cleaner must keep the line, then the multi-platform reader reads it. Where the feed supplies
structured truth (MLB Stats API: event type, batted-ball trajectory,
fielder position), BLE's reading is scored against it. Every feed is
also checked for unread plays: no event, no batter, a ball in play
with no ball type, or a fielder named in the text but no location.

Plays are grouped by phrasing template (player names and numbers
masked) so one fix can be judged by how many real plays it covers.

Usage:
    py -m tools.language_audit.audit <corpus.jsonl> <feed> [report.md]

feed: mlb_statsapi | espn
"""

from __future__ import annotations

import collections
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

from cleaners.college_cleaner import clean_college_text
from cleaners.mlb_cleaner import clean_mlb_text
from language.normalizer import normalize_play_text
from language.reader import build_multi_platform_plate_appearance
from models.types import EventType


K_EVENTS = {
    EventType.STRIKEOUT,
    EventType.STRIKEOUT_LOOKING,
    EventType.STRIKEOUT_SWINGING,
    EventType.DROPPED_THIRD_STRIKE_REACH,
    EventType.DROPPED_THIRD_STRIKE_OUT,
}

HIT_EVENTS = {
    EventType.SINGLE: "1B",
    EventType.DOUBLE: "2B",
    EventType.TRIPLE: "3B",
    EventType.HOME_RUN: "HR",
}

RUNNER_ONLY = {
    EventType.STOLEN_BASE,
    EventType.CAUGHT_STEALING,
    EventType.PICKOFF,
    EventType.RUNNER_OUT,
    EventType.WILD_PITCH_ADVANCE,
    EventType.PASSED_BALL_ADVANCE,
}


# ---------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------

_NAME = r"(?:[A-Z][A-Za-z'’.\-À-ſ]*|Mc[A-Z][a-z]+|de|De|la|La|van|Van|del|St\.)"
_NAME_RUN = re.compile(
    rf"\b{_NAME}(?:\s+{_NAME})*(?:,\s*{_NAME}(?:\s+{_NAME})*)?"
    rf"(?:\s+(?:Jr\.?|Sr\.?|II|III|IV))?"
)


def template(text: str) -> str:
    t = text.strip()
    t = re.sub(r"\((\d-\d)(?: [A-Z]*)?\)", "(COUNT)", t)
    t = re.sub(r"\(\d+\)", "(#)", t)
    t = _NAME_RUN.sub("<N>", t)
    t = re.sub(r"\d+", "#", t)
    return re.sub(r"\s+", " ", t)


# ---------------------------------------------------------------------
# Truth
# ---------------------------------------------------------------------

_MLB_IN_PLAY = {
    "field_out", "force_out", "grounded_into_double_play", "double_play",
    "triple_play", "sac_fly", "sac_bunt", "field_error", "fielders_choice",
    "fielders_choice_out", "sac_fly_double_play", "sac_bunt_double_play",
}

_MLB_TRAJECTORY = {
    "ground_ball": "GB",
    "line_drive": "FB",
    "fly_ball": "FB",
    "popup": "FB",
    "bunt_grounder": "BUNT",
    "bunt_popup": "BUNT",
    "bunt_line_drive": "BUNT",
}

_MLB_POSITION = {
    "1": "P", "2": "C", "3": "1B", "4": "2B", "5": "3B",
    "6": "SS", "7": "LF", "8": "CF", "9": "RF",
}


def mlb_truth(row: dict) -> dict | None:
    event_type = row.get("eventType") or ""

    if event_type in {"strikeout", "strikeout_double_play"}:
        outcome = "K"
    elif event_type in {"walk", "intent_walk"}:
        outcome = "BB"
    elif event_type == "hit_by_pitch":
        outcome = "HBP"
    elif event_type in {"single", "double", "triple", "home_run"}:
        outcome = {"single": "1B", "double": "2B", "triple": "3B", "home_run": "HR"}[event_type]
    elif event_type in _MLB_IN_PLAY:
        outcome = "BIP"
    elif event_type == "catcher_interf":
        outcome = "CI"
    else:
        return None

    location = row.get("hit_location")

    return {
        "outcome": outcome,
        "ball_type": _MLB_TRAJECTORY.get(row.get("trajectory") or ""),
        "location": _MLB_POSITION.get(location) if location and len(location) == 1 else None,
    }


# ESPN labels the pitch that ended the plate appearance ("Pitch 4 :
# Ball In Play" typed "Ground Out"). Only those labelled plays get truth.
_ESPN_LABELS = {
    "Ground Out": ("BIP", "GB"),
    "Fly Out": ("BIP", "FB"),
    "Line Out": ("BIP", "FB"),
    "Pop Out": ("BIP", "FB"),
    "Foul Out": ("BIP", "FB"),
    "Bunt Ground Out": ("BIP", "BUNT"),
    "Bunt Pop Out": ("BIP", "BUNT"),
    "Bunt Single": ("1B", "BUNT"),
    "Sacrifice": ("BIP", "BUNT"),
    "Sacrifice Fly": ("BIP", "FB"),
    "Single": ("1B", None),
    "Double": ("2B", None),
    "Ground Rule Double": ("2B", None),
    "Triple": ("3B", None),
    "Home Run": ("HR", None),
    "Hit By Pitch": ("HBP", None),
    "Batters Fielders Choice - Runner Out": ("BIP", None),
    "Batters Fielders Choice - All Runners Safe": ("BIP", None),
    "Batter Reached On Error - Batter To First": ("BIP", None),
}


def espn_truth(previous: dict) -> dict | None:
    label = previous.get("type")
    text = previous.get("text") or ""

    if label in _ESPN_LABELS:
        outcome, ball_type = _ESPN_LABELS[label]
    elif label in {"Strike Swinging", "Strike Looking"} and "Strike 3" in text:
        outcome, ball_type = "K", None
    elif label == "Ball" and "Ball 4" in text:
        outcome, ball_type = "BB", None
    else:
        return None

    return {"outcome": outcome, "ball_type": ball_type, "location": None}


# ---------------------------------------------------------------------
# BLE reading
# ---------------------------------------------------------------------

CLEANERS = {
    "mlb_statsapi": clean_mlb_text,
    "espn": clean_college_text,
}


def ble_reading(text: str, feed: str) -> dict:
    kept = CLEANERS[feed](text)

    if not kept:
        return {
            "event": None, "outcome": "DROPPED", "batter": None,
            "ball_type": None, "location": None, "is_bip": False,
        }

    pa = build_multi_platform_plate_appearance(kept[0])
    event = pa.baseball_event.primary_event if pa.baseball_event else None

    if event in K_EVENTS:
        outcome = "K"
    elif event == EventType.WALK:
        outcome = "BB"
    elif event == EventType.HIT_BY_PITCH:
        outcome = "HBP"
    elif event == EventType.CATCHER_INTERFERENCE:
        outcome = "CI"
    elif event in HIT_EVENTS:
        outcome = HIT_EVENTS[event]
    elif pa.is_bip:
        outcome = "BIP"
    elif event in RUNNER_ONLY:
        outcome = "RUNNER"
    else:
        outcome = None

    return {
        "event": event.value if event else None,
        "outcome": outcome,
        "batter": pa.batter_name,
        "ball_type": pa.ball_type,
        "location": pa.location,
        "is_bip": pa.is_bip,
    }


_POSITION_WORD_RE = re.compile(
    r"\b(pitcher|catcher|first base(?:man)?|second base(?:man)?|third base(?:man)?|"
    r"shortstop|left field(?:er)?|center field(?:er)?|right field(?:er)?|"
    r"left|center|right|middle|"
    r"p|c|1b|2b|3b|ss|lf|cf|rf)\b",
    re.I,
)

_TRAJECTORY_RE = re.compile(
    r"\b(ground(?:s|ed)?|grounder|fl(?:y|ies|ied)|line(?:s|d)?|liner|pop(?:s|ped)?|popup|"
    r"foul(?:s|ed)? out|bunt(?:s|ed)?|sacrifice|sac)\b",
    re.I,
)

def _states_trajectory(text: str) -> bool:
    normalized = re.sub(r"ground-rule double", "", normalize_play_text(text), flags=re.I)
    return bool(_TRAJECTORY_RE.search(normalized))


_BATTED_RE = re.compile(
    r"\b(single|double|triple|homer|ground|grounded|fl(?:y|ies|ied)|line|lined|pop|popped|"
    r"foul(?:ed)? out|bunt|sacrifice|error|fielder's choice|double play|infield)\w*",
    re.I,
)


# ---------------------------------------------------------------------
# Corpus loading
# ---------------------------------------------------------------------

@dataclass
class Play:
    text: str
    truth: dict | None = None


def load_plays(path: Path, feed: str) -> list[Play]:
    plays: list[Play] = []
    previous: dict = {}

    for line in path.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)

        if feed == "mlb_statsapi":
            if row.get("kind") != "pa" or not row.get("description"):
                continue
            truth = mlb_truth(row)
            if truth is not None:
                truth["batter"] = row.get("batter")
            plays.append(Play(text=row["description"], truth=truth))

        elif feed == "espn":
            if row.get("type") != "Play Result" or not row.get("text"):
                previous = row
                continue
            plays.append(Play(text=row["text"], truth=espn_truth(previous)))
            previous = row

    return plays


# ---------------------------------------------------------------------
# Audit
# ---------------------------------------------------------------------

@dataclass
class TemplateStats:
    count: int = 0
    issues: collections.Counter = field(default_factory=collections.Counter)
    examples: dict = field(default_factory=dict)


def _issues(play: Play, reading: dict) -> list[str]:
    issues: list[str] = []
    truth = play.truth

    if truth is not None:
        if reading["outcome"] != truth["outcome"]:
            issues.append(f"outcome {truth['outcome']}->{reading['outcome']}")

        if truth["ball_type"] and reading["ball_type"] != truth["ball_type"]:
            if reading["ball_type"] is None and not _states_trajectory(play.text):
                pass  # text does not say how the ball was hit
            elif reading["ball_type"] is None:
                issues.append("ball_type missing")
            else:
                issues.append(f"ball_type {truth['ball_type']}->{reading['ball_type']}")

        # "to left fielder X, deflected by shortstop Y": the feed credits
        # the deflecting fielder; BLE keeps where the ball went.
        deflected = "deflected by" in play.text
        if truth["location"] and reading["location"] != truth["location"] and not deflected:
            if reading["location"] is None:
                issues.append("location missing")
            else:
                issues.append(f"location {truth['location']}->{reading['location']}")

        if not reading["batter"]:
            issues.append("batter missing")
        elif truth.get("batter") and reading["batter"] != truth["batter"]:
            issues.append("batter wrong")

        if truth["outcome"] in {"K", "BB", "HBP", "CI"} and reading["location"]:
            issues.append(f"location on non-BIP ({reading['location']})")

        return issues

    if reading["outcome"] == "DROPPED":
        # Runner-only advances ("advanced to second on an error by p,
        # failed pickoff attempt") carry no batter stat.
        if re.search(r"\b(?:advanced|to second|to third)\b", play.text) and not re.search(
            r"\b(?:stole|caught stealing|singled|doubled|walked|hit a|homered)\b", play.text
        ):
            return issues
        if _BATTED_RE.search(play.text) or re.search(r"(walk|struck|strikes|hit by|steal|stole)", play.text, re.I):
            issues.append("dropped by cleaner")
        return issues

    if reading["outcome"] is None:
        if _BATTED_RE.search(play.text) or re.search(r"\b(walk|struck|strikes|hit by)", play.text, re.I):
            issues.append("unread")
        return issues

    if reading["outcome"] != "RUNNER" and not reading["batter"]:
        issues.append("batter missing")

    if reading["is_bip"] and reading["ball_type"] is None:
        # Only a misread when the text actually states how the ball
        # was hit. "singled to left" stays unknown by design.
        if _states_trajectory(play.text):
            issues.append("BIP without ball_type")

    if reading["is_bip"] and reading["location"] is None and _POSITION_WORD_RE.search(play.text):
        issues.append("BIP without location")

    if reading["outcome"] in {"K", "BB", "HBP"} and reading["location"]:
        issues.append(f"location on non-BIP ({reading['location']})")

    return issues


def audit(plays: list[Play], feed: str) -> tuple[dict[str, TemplateStats], collections.Counter]:
    by_template: dict[str, TemplateStats] = collections.defaultdict(TemplateStats)
    totals: collections.Counter = collections.Counter()

    for play in plays:
        reading = ble_reading(play.text, feed)
        issues = _issues(play, reading)

        key = template(play.text)
        stats = by_template[key]
        stats.count += 1
        totals["plays"] += 1

        if issues:
            totals["plays_with_issues"] += 1

        for issue in issues:
            kind = issue.split(" ")[0] if "->" in issue else issue
            totals[kind] += 1
            stats.issues[issue] += 1
            stats.examples.setdefault(issue, (play.text, reading))

    return by_template, totals


def render_report(name: str, by_template: dict[str, TemplateStats], totals: collections.Counter, limit: int = 120) -> str:
    lines = [f"# Language audit: {name}", ""]
    plays = totals["plays"] or 1
    clean = plays - totals["plays_with_issues"]
    lines.append(f"Plays: {totals['plays']}  |  read cleanly: {clean} ({clean / plays:.1%})")
    lines.append("")

    for key, value in sorted(totals.items(), key=lambda kv: -kv[1]):
        if key in {"plays", "plays_with_issues"}:
            continue
        lines.append(f"- {key}: {value}")

    lines += ["", "## Failing phrasings (most plays first)", ""]

    ranked = sorted(
        ((sum(s.issues.values()), key, s) for key, s in by_template.items() if s.issues),
        key=lambda item: -item[0],
    )

    for affected, key, stats in ranked[:limit]:
        lines.append(f"### {affected} issues / {stats.count} plays: `{key}`")
        for issue, count in stats.issues.most_common(4):
            text, reading = stats.examples[issue]
            lines.append(f"- {count}x **{issue}** e.g. `{text}` -> {reading}")
        lines.append("")

    return "\n".join(lines)


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print(__doc__)
        return 1

    path = Path(argv[1])
    feed = argv[2]

    by_template, totals = audit(load_plays(path, feed), feed)
    report = render_report(path.name, by_template, totals)

    if len(argv) > 3:
        Path(argv[3]).write_text(report, encoding="utf-8")

    print(report.split("## Failing")[0])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
