"""
Read one plate appearance from any non-GameChanger platform.

The legacy detectors (frozen for GameChanger) run first on the
normalized text. This reader then fills the gaps other platforms
expose:

- past-tense / alternate phrasings the legacy detector does not know
  ("popped up", "reached on a throwing error", "hits a grand slam")
- generic outcomes with no subtype ("struck out", "out at first")
- catcher's interference (not a ball in play, not a K/BB/HBP)
- batter names for phrasings the legacy extractor misses, and the
  batter (not the pitcher) on "X intentionally walks Y"
- fielder location read from the batter's own clause only, so runner
  clauses ("Jones advanced to second") never become a hit location
- the true fielder on pitcher-started plays ("grounds out, pitcher X
  to first baseman Y" is a ball fielded by the pitcher)
- no location on outcomes that are not balls in play

Rule kept from the legacy engine: never invent data. A ball type is
only set when the text says how the ball was hit.
"""

from __future__ import annotations

import re

from assemblers.pitch_decision_builder import build_pitch_decisions
from classifiers import ball_type_classifier
from classifiers.bip_classifier import is_ball_in_play
from detectors import event_detector
from extractors import player_extractor
from extractors.pitch_token_extractor import extract_pitch_tokens
from language.normalizer import PITCH_SEQUENCE_RE, normalize_play_text
from language.result_labels import result_label
from models.baseball_event import BaseballEvent
from models.detected_event import DetectedEvent
from models.pitch_decision import PitchDecision
from models.plate_appearance import PlateAppearance
from models.runner_event import RunnerEvent
from models.types import EventType
from translators.base_translator import detected_events_to_baseball_event


RUNNER_ONLY_EVENTS = {
    EventType.STOLEN_BASE,
    EventType.CAUGHT_STEALING,
    EventType.PICKOFF,
    EventType.RUNNER_OUT,
    EventType.WILD_PITCH_ADVANCE,
    EventType.PASSED_BALL_ADVANCE,
}

STRIKEOUT_EVENTS = {
    EventType.STRIKEOUT,
    EventType.STRIKEOUT_LOOKING,
    EventType.STRIKEOUT_SWINGING,
    EventType.DROPPED_THIRD_STRIKE_REACH,
    EventType.DROPPED_THIRD_STRIKE_OUT,
}

_RESULT_HEADERS = {
    "runner out",
    "sacrifice bunt",
}


# ---------------------------------------------------------------------
# Action text
# ---------------------------------------------------------------------

def _action_text(pa_block: str) -> str:
    lines = [line.strip() for line in str(pa_block or "").splitlines() if line.strip()]

    if not lines:
        return ""

    if lines[0].lower() in _RESULT_HEADERS and len(lines) > 1:
        return " ".join(lines[1:])

    return lines[-1]


# ---------------------------------------------------------------------
# Events
# ---------------------------------------------------------------------

# Batter outcomes the legacy detector does not recognize. Checked in
# order; the first match becomes the primary event when the legacy
# detector found no batter outcome.
_BATTER_OUTCOME_RULES: list[tuple[re.Pattern, EventType]] = [
    (re.compile(r"\bcatcher'?s? interference\b", re.I), EventType.CATCHER_INTERFERENCE),
    (re.compile(r"\bhits? a grand slam\b", re.I), EventType.HOME_RUN),
    (re.compile(r"\binside the park home run\b", re.I), EventType.HOME_RUN),
    (re.compile(r"\bground-rule double\b", re.I), EventType.DOUBLE),
    (re.compile(r"\bbunt single\b", re.I), EventType.SINGLE),
    (
        re.compile(
            r"\b(?:reach(?:es|ed)|safe at (?:first|second|third|home)|safe) on (?:a |an )?"
            r"(?:(?:fielding|throwing|missed catch|dropped fly|catching) )?(?:error|muffed throw|muff)\b",
            re.I,
        ),
        EventType.ERROR,
    ),
    (re.compile(r"\bsafe at first on (?:a )?fielder'?s choice\b", re.I), EventType.FIELDERS_CHOICE),
    (re.compile(r"\binto (?:a )?force out\b", re.I), EventType.FIELDERS_CHOICE),
    # "sacrified" is a real ESPN misspelling.
    (re.compile(r"\bsacrifi(?:c)?ed\b|\bsac bunt\b", re.I), EventType.SAC_BUNT),
    # StatCrew: "Smith out at first 1b to 2b, SAC, bunt".
    (re.compile(r"\bSAC\b"), EventType.SAC_BUNT),
    # No separate triple-play stat; it is a ball in play like a DP.
    (re.compile(r"\btriple play\b", re.I), EventType.DOUBLE_PLAY),
    (re.compile(r"\bintentional(?:ly)? walk", re.I), EventType.WALK),
    (re.compile(r"\b(?:struck|strikes) out\b", re.I), EventType.STRIKEOUT),
    (re.compile(r"\bfoul(?:s|ed)? out\b", re.I), EventType.POP_OUT),
    (re.compile(r"\bpop(?:s|ped)? up\b", re.I), EventType.POP_OUT),
    # "Smith out at first 1b to p" — the batter retired on a batted ball
    # with no ball type stated.
    (re.compile(r"^[^;]*?\bout at first\b", re.I), EventType.FIELD_OUT),
]

_CAUGHT_STEALING_RE = re.compile(r"\bcaught stealing\b", re.I)
_PICKED_OFF_RE = re.compile(r"\bpicked off\b", re.I)


# A line that opens with a runner action is a runner play, whatever
# follows ("Johnson stole second, Johnson safe at third on error").
_RUNNER_LEAD_RE = re.compile(
    r"^(?:[A-Z#][\w'.,\-]*\s+){1,5}"
    r"(?:stole|steals|advanced|advances|to (?:first|second|third|home|1st|2nd|3rd)\b|"
    r"caught stealing|picked off|scored|scores|out at (?:second|third|home)|failed pickoff)"
)


def _detect_events(text: str) -> list[DetectedEvent]:
    # Looked up on the module at call time so applications that patch
    # BLE detectors at runtime (Opponent IQ's iScore support) still apply.
    events = event_detector.detect_event_types(text)

    # "grounded into fielder's choice": the legacy detector marks the
    # groundout primary; the batter actually reached on the FC.
    primary = next((event for event in events if event.is_primary), None)
    fielders_choice = next(
        (event for event in events if event.event_type == EventType.FIELDERS_CHOICE), None
    )
    if primary is not None and fielders_choice is not None and primary.event_type in {
        EventType.GROUND_OUT, EventType.FLY_OUT, EventType.LINE_OUT, EventType.POP_OUT,
    }:
        primary.is_primary = False
        fielders_choice.make_primary()
        events.remove(fielders_choice)
        events.insert(0, fielders_choice)

    has_batter_outcome = any(event.is_primary for event in events)

    if not has_batter_outcome and not _RUNNER_LEAD_RE.search(text):
        for pattern, event_type in _BATTER_OUTCOME_RULES:
            if pattern.search(text):
                outcome = DetectedEvent(event_type=event_type)
                outcome.make_primary()

                # A pickoff or caught-stealing line that also says
                # "out at first" is still a runner play.
                if event_type == EventType.FIELD_OUT and (
                    _PICKED_OFF_RE.search(text) or _CAUGHT_STEALING_RE.search(text)
                ):
                    break

                events.insert(0, outcome)
                break

    detected_types = {event.event_type for event in events}

    # Legacy runner checks need a trailing space ("caught stealing ").
    # Platforms that end the clause with punctuation are read here.
    if EventType.CAUGHT_STEALING not in detected_types and _CAUGHT_STEALING_RE.search(text):
        events.append(DetectedEvent(event_type=EventType.CAUGHT_STEALING))

    if EventType.PICKOFF not in detected_types and _PICKED_OFF_RE.search(text):
        events.append(DetectedEvent(event_type=EventType.PICKOFF))

    return events


# ---------------------------------------------------------------------
# Batter
# ---------------------------------------------------------------------

_INTENTIONAL_WALK_RE = re.compile(
    r"^(?P<pitcher>.+?)\s+intentionally walks\s+(?P<batter>.+)$",
)

# End of the walked batter's name: a sentence period (after two
# lowercase letters, so "J.P." and "Jr." survive), a comma or semicolon.
_NAME_END_RE = re.compile(r"(?<=[a-zß-ÿ]{2})\.(?=\s|$)|[,;]")

# Lowercase verbs, matched case-sensitively so names never collide.
_BATTER_VERBS = [
    "singles", "doubles", "triples", "homers",
    "singled", "doubled", "tripled", "homered",
    "hits", "hit into", "hit sacrifice", "hit by pitch", "hit a ground-rule",
    "grounds", "grounded", "flies", "flied", "lines", "lined",
    "pops", "popped", "fouls", "fouled", "bunts", "bunted",
    "bunt grounds", "bunt pops", "bunt lines", "bunt flies",
    "strikes out", "struck out", "called out on strikes",
    "walks", "walked", "intentionally walked", "is walked",
    "is hit by", "reaches", "reached", "safe at first",
    "is intentionally walked", "is picked off", "is caught stealing",
    "infield fly",
    "out on a sacrifice", "out on sacrifice", "out on infield fly",
    "out at first", "is out", "sacrifices", "sacrificed", "sacrified",
    "safe at second", "safe at third",
]

_BATTER_VERB_RE = re.compile(
    r"\s(" + "|".join(sorted((re.escape(verb) for verb in _BATTER_VERBS), key=len, reverse=True)) + r")\b"
)


def _clean_name(name: str | None) -> str | None:
    if not name:
        return None

    cleaned = re.sub(r"\s+", " ", name).strip(" ,;:")
    # "M. Caputo was picked off" -> "M. Caputo"
    cleaned = re.sub(r"\s+(?:was|is|has|had)$", "", cleaned)

    # iScore: "Ball 4. #12 John Smith" / "#12 John Smith" -> "John Smith".
    if "#" in cleaned:
        cleaned = re.sub(r"^#\d+\s*", "", cleaned[cleaned.rindex("#"):])

    return cleaned or None


def _extract_batter(text: str, primary: EventType | None) -> str | None:
    if primary is None or primary in RUNNER_ONLY_EVENTS:
        return None

    intentional = _INTENTIONAL_WALK_RE.search(text)
    if intentional:
        batter = intentional.group("batter")
        end = _NAME_END_RE.search(batter)
        if end:
            batter = batter[: end.start()]
        # "Michael Harris II." ends the sentence; "Luis Robert Jr." keeps it.
        batter = re.sub(r"\b(II|III|IV)\.$", r"\1", batter.strip())
        return _clean_name(batter)

    match = _BATTER_VERB_RE.search(text)
    if match:
        return _clean_name(text[: match.start()])

    return _clean_name(player_extractor.extract_batter_name(text))


# ---------------------------------------------------------------------
# Location
# ---------------------------------------------------------------------

# Earliest fielder/direction named in the batter's own clause wins.
_LOCATION_PATTERNS: list[tuple[str, str]] = [
    (r"left[- ]center", "LF"),
    (r"right[- ]center", "RF"),
    (r"left field(?:er)?", "LF"),
    (r"right field(?:er)?", "RF"),
    (r"center field(?:er)?", "CF"),
    (r"to left\b", "LF"),
    (r"to right\b", "RF"),
    (r"to center\b", "CF"),
    (r"third base(?:man)?", "3B"),
    (r"to third\b", "3B"),
    (r"shortstop", "SS"),
    (r"second base(?:man)?", "2B"),
    (r"to second\b", "2B"),
    (r"first base(?:man)?", "1B"),
    (r"to first\b", "1B"),
    (r"pitcher", "P"),
    (r"back to the mound", "P"),
    (r"catcher", "C"),
]

_LOCATION_RE = [(re.compile(rf"\b{pattern}", re.I), location) for pattern, location in _LOCATION_PATTERNS]

_SENTENCE_SPLIT_RE = re.compile(r"(?<=[a-z0-9)]{2})\s?\.\s+(?=[A-Z#])|;\s*")

# ", Jones advanced to second" / ", Jones to third" / ", Jones scored"
# / ", Jones out at second" — runner clauses inside the batter sentence.
_RUNNER_CLAUSE_RE = re.compile(
    r",\s*(?:[A-Z][\w'.\-]*\.?,?\s+){1,4}"
    r"(?:advanced to|advances to|to|scored|scores|out at|stole|steals|remains at)\b[^,;]*",
)

# "pitcher" on its own is a fielder; "pitching" and "pitches" are not.
# A pitcher clause such as "Smith pitching" is removed before reading.
_PITCHING_CLAUSE_RE = re.compile(r",\s*[^,;]*\bpitching\b[^,;]*", re.I)


def batter_clause(text: str) -> str:
    # Sentence ends are only searched after the batter's verb, so an
    # abbreviated name ("Jal. Flores", "Pearson, Js.") is never split.
    verb = _BATTER_VERB_RE.search(text)
    start = verb.end() if verb else 0

    boundary = _SENTENCE_SPLIT_RE.search(text, start)
    first_sentence = text[: boundary.start()] if boundary else text

    # Runner clauses are only removed after the verb so the batter's
    # own "Last, F." name is never mistaken for one.
    head, tail = first_sentence[:start], first_sentence[start:]
    tail = _RUNNER_CLAUSE_RE.sub("", tail)
    return head + _PITCHING_CLAUSE_RE.sub("", tail)


def _earliest_location(text: str) -> str | None:
    candidates = []
    for pattern, location in _LOCATION_RE:
        match = pattern.search(text)
        if match:
            candidates.append((match.start(), location))

    if not candidates:
        return None

    return min(candidates, key=lambda item: item[0])[1]


# "Jones out at second shortstop to second baseman" — the first fielder
# of a force chain is the fielder who played the batted ball.
_FORCE_CHAIN_RE = re.compile(
    r"\bout at (?:first|second|third|home)\s+(?P<chain>(?:pitcher|catcher|first baseman|"
    r"second baseman|third baseman|shortstop|left fielder|center fielder|right fielder)\b[^,;.]*)",
)

_FORCE_CHAIN_EVENTS = {
    EventType.FIELDERS_CHOICE,
    EventType.FC_DOUBLE_PLAY,
    EventType.DOUBLE_PLAY,
}


def classify_fielder_location(text: str, primary: EventType | None = None) -> str | None:
    location = _earliest_location(batter_clause(text))

    if location is None and primary in _FORCE_CHAIN_EVENTS:
        chain = _FORCE_CHAIN_RE.search(text)
        if chain:
            location = _earliest_location(chain.group("chain"))

    # iScore names the fielder in a second sentence:
    # "grounds out . Unassisted out by first baseman ."
    if location is None:
        putout = _PUTOUT_BY_RE.search(text)
        if putout:
            location = _earliest_location(putout.group("fielder"))

    return location


_PUTOUT_BY_RE = re.compile(
    r"\b(?:unassisted )?out by (?:the )?(?P<fielder>pitcher|catcher|first baseman|second baseman|"
    r"third baseman|shortstop|left fielder|center fielder|right fielder)\b",
    re.I,
)


# ---------------------------------------------------------------------
# Ball type
# ---------------------------------------------------------------------

_EXTRA_BALL_TYPE_RULES: list[tuple[re.Pattern, str]] = [
    (re.compile(r"\bbunt", re.I), "BUNT"),
    # A sacrifice that is not a sacrifice fly is a bunt.
    (re.compile(r"\bsacrifi(?:c)?ed\b|\bsac bunt\b", re.I), "BUNT"),
    (re.compile(r"\bSAC\b"), "BUNT"),
    (re.compile(r"\bgrounder\b", re.I), "GB"),
    (re.compile(r"\bfoul(?:s|ed)? out\b|\bfoul (?:fly|pop)", re.I), "FB"),
    (re.compile(r"\bpop(?:s|ped)? (?:up|into)\b|\bpopup\b|\bpop-up\b", re.I), "FB"),
    (re.compile(r"\bliner\b", re.I), "FB"),
]


def _classify_ball_type(text: str) -> str | None:
    ball_type = ball_type_classifier.classify_ball_type(text)

    if ball_type is not None:
        return ball_type

    for pattern, value in _EXTRA_BALL_TYPE_RULES:
        if pattern.search(text):
            return value

    return None


# ---------------------------------------------------------------------
# Runner events
# ---------------------------------------------------------------------

# Case-sensitive, accent-aware runner names: a run of capitalized
# tokens (plus lowercase surname particles), so "strikes out swinging
# and Trea Turner" yields "Trea Turner" and "Julio Rodríguez" stays whole.
_NAME_START = r"[A-Z\u00C0-\u00DE]"
_NAME_TOKEN = rf"(?:{_NAME_START}[\w'.\-]*|de|del|la|las|los|da|das|do|dos|di|van|von|le)"
# iScore runners carry a jersey prefix: "#12 John Smith steals second".
_RUNNER_NAME = rf"(?:#\d+\s+)?{_NAME_START}[\w'.\-]*(?:,?\s+(?:{_NAME_TOKEN}|\d+\b))*"

_BASE_WORDS = {
    "second": "2B", "2nd": "2B", "2b": "2B",
    "third": "3B", "3rd": "3B", "3b": "3B",
    "home": "HOME",
}

_BASE = r"(?P<base>second|2nd|2b|third|3rd|3b|home)\b"
_STEAL_TOTAL = r"(?:\(\d+\)\s+)?"

_RUNNER_RULES: list[tuple[re.Pattern, str]] = [
    (re.compile(rf"(?P<runner>{_RUNNER_NAME})\s+(?:steals|stole|steal)\s+{_STEAL_TOTAL}{_BASE}"), "SB"),
    (
        re.compile(
            rf"(?P<runner>{_RUNNER_NAME})\s+(?:is\s+)?(?:picked off and )?caught stealing\s+{_STEAL_TOTAL}{_BASE}"
        ),
        "CS",
    ),
    # "Smith out at second c to ss, caught stealing."
    (
        re.compile(
            rf"(?P<runner>{_RUNNER_NAME})\s+out at {_BASE}[^;.]*?caught stealing"
        ),
        "CS",
    ),
]

# A prior sentence glued to the name: "Joe Ryan. Sal Frelick" -> "Sal Frelick".
# Initials ("J. Smith", "J.P. Crawford") are not sentence ends.
_PRIOR_SENTENCE_RE = re.compile(r"^.*(?<=[a-z\u00DF-\u00FF]{2})[.!?]\s+")


def _runner_name(raw: str) -> str | None:
    name = _PRIOR_SENTENCE_RE.sub("", raw.strip())
    return _clean_name(name)


def _extract_runner_events(text: str) -> list[RunnerEvent]:
    found: list[tuple[int, RunnerEvent]] = []
    seen: set[tuple[str, str | None, str]] = set()

    for pattern, event_type in _RUNNER_RULES:
        for match in pattern.finditer(text):
            runner = _runner_name(match.group("runner"))
            base = _BASE_WORDS[match.group("base").lower()]
            key = (event_type, runner, base)

            if key in seen:
                continue

            seen.add(key)
            found.append(
                (
                    match.start(),
                    RunnerEvent(event_type=event_type, base=base, runner_name=runner),
                )
            )

    return [event for _, event in sorted(found, key=lambda item: item[0])]


# ---------------------------------------------------------------------
# Pitches
# ---------------------------------------------------------------------

# StatCrew pitch codes. Unknown codes stop the decode rather than guess.
_STATCREW_PITCH_CODES = {
    "B": "Ball 1",
    "K": "Strike 1 looking",
    "S": "Strike 1 swinging",
    "F": "Foul",
}


def _statcrew_pitch_tokens(raw_text: str, is_bip: bool) -> list[str]:
    match = PITCH_SEQUENCE_RE.search(raw_text)

    if not match:
        return []

    tokens: list[str] = []

    for code in match.group("sequence") or "":
        token = _STATCREW_PITCH_CODES.get(code)
        if token is None:
            return []
        tokens.append(token)

    # The sequence lists every pitch before the ball put in play.
    if is_bip:
        tokens.append("In play")

    return tokens


def _pitch_decisions(pa_block: str, action_text: str, is_bip: bool):
    # Pitch lines only. The play sentence itself is never read for
    # pitch tokens ("fouled out" is not a foul ball).
    pitch_lines = [
        line
        for line in str(pa_block or "").splitlines()
        if line.strip() and line.strip() != action_text
    ]
    tokens = extract_pitch_tokens(pitch_lines)

    if not tokens:
        tokens = _statcrew_pitch_tokens(action_text, is_bip)

    return build_pitch_decisions(tokens)


# ---------------------------------------------------------------------
# Plate appearance
# ---------------------------------------------------------------------

def _split_result_label(pa_block: str):
    """
    Pull an app result label line ("Ground Out", "Bunt Single") out of
    the block, and drop PlayMaker's separate "Scored ..." line, so the
    play sentence is what gets read.
    """
    label = None
    kept = []

    for line in str(pa_block or "").splitlines():
        stripped = line.strip()
        found = result_label(stripped) if stripped else None

        if found is not None and label is None:
            label = found
            continue

        if stripped.lower().startswith("scored") and kept:
            continue

        kept.append(line)

    return label, "\n".join(kept) if kept else str(pa_block or "")


# "John Smith #12 ..." / "John Smith ..." -> "John Smith"
_LEADING_NAME_RE = re.compile(
    r"^((?:[A-ZÀ-Þ][\w'.\-]*\s+){1,3}[A-ZÀ-Þ][\w'.\-]*)(?=\s+(?:#\d+|[a-z]))"
)


def _leading_name(sentence: str) -> str | None:
    match = _LEADING_NAME_RE.match(str(sentence or "").strip())
    return _clean_name(match.group(1)) if match else None


def build_multi_platform_plate_appearance(
    pa_block: str,
    pitches: list[PitchDecision] | None = None,
) -> PlateAppearance:
    """
    pitches: decisions supplied by the source (MLB StatsAPI pitch data).
    When given they are used as-is instead of reading pitch text.
    """
    label, pa_block = _split_result_label(pa_block)

    raw_action = _action_text(pa_block)
    text = normalize_play_text(raw_action)

    detected = _detect_events(text)
    baseball_event: BaseballEvent | None = detected_events_to_baseball_event(detected)

    # The app's own result label decides only when the sentence itself
    # gave no outcome.
    if baseball_event is None and label is not None:
        baseball_event = BaseballEvent(primary_event=label[0], secondary_events=[])

    primary = baseball_event.primary_event if baseball_event else None

    is_bip = is_ball_in_play(baseball_event)

    batter_name = _extract_batter(text, primary)
    if batter_name is None and label is not None:
        batter_name = _leading_name(raw_action)

    runner_events = _extract_runner_events(text)

    ball_type = _classify_ball_type(batter_clause(text)) if is_bip else None
    if ball_type is None and is_bip and label is not None:
        ball_type = label[1]

    location = classify_fielder_location(text, primary) if is_bip else None

    if pitches is None:
        pitches = _pitch_decisions(pa_block, raw_action, is_bip)

    return PlateAppearance(
        batter_name=batter_name,
        baseball_event=baseball_event,
        pitches=pitches,
        runner_events=runner_events,
        ball_type=ball_type,
        location=location,
        is_bip=is_bip,
    )


__all__ = [
    "batter_clause",
    "build_multi_platform_plate_appearance",
    "classify_fielder_location",
]
