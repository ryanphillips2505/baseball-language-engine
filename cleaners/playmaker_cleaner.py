"""
PlayMaker (play.playmakerapp.io) game page text, as a coach copies it.

The page lists half innings newest first ("Top 9th" ... "Top 1st"), each
play as a result label line ("Ground Out") and a sentence ("José Rondón #9
grounded out to shortstop AS: Juan Villavicencio #7 PO: Jose Salas #3"),
sometimes followed by "Scored: ..." / "Moved on basepath: ..." lines. After
the plays come the scoreboard, both batting / pitching boxes and a scoring
summary that repeats scoring plays; those are never read as plays.

Blocks come out in game order, one per play: "Label\\nSentence[\\nmore]".
"""

from __future__ import annotations

import re

from language.result_labels import result_label


_HALF_RE = re.compile(r"^(top|bottom)\s+(\d+)(?:st|nd|rd|th)$", re.I)
_CONTINUATION_RE = re.compile(r"^(?:scored:|moved on basepath:|out on the basepath:)", re.I)
# "Marvin Alcántara #21" -> "Marvin Alcántara": BLE's name reader treats a
# "#" as an iScore jersey prefix and would drop the name.
_JERSEY_SUFFIX_RE = re.compile(r"\s+#\d+\b")
# PlayMaker credits fielders after the play: "AS: A #7 PO: B #3".
_FIELDER_CREDITS_RE = re.compile(r"\s+(?:AS|PO):\s.*?(?=\s+(?:AS|PO):\s|$)")

# PlayMaker also prints a plain "Bunt" label (not in the outcome table).
_EXTRA_LABELS = {"bunt"}

_PLAYMAKER_MARKER_RE = re.compile(
    r"(?m)(?:\bMoved on basepath:|\bOut on the basepath:|\s(?:AS|PO):\s)"
)
_PLAYMAKER_SENTENCE_RE = re.compile(
    r"(?m)^[A-ZÀ-Þ][^\n#]{1,40}\s#\d+\s+(?:grounded|flew|lined|popped|struck|walked|"
    r"singled|doubled|tripled|homered|hit into|reached|was|sac|bunted|fouled|stole)\b"
)


def _is_label(line: str) -> bool:
    return result_label(line) is not None or " ".join(line.lower().split()) in _EXTRA_LABELS


_PAST_TENSE_PLAY_RE = re.compile(
    r"^[A-ZÀ-Þ][^\n]{0,60}?\s(?:grounded|flew|lined|popped|struck|walked|singled|"
    r"doubled|tripled|homered|hit into|reached|was|sac|sacrificed|bunted|fouled|"
    r"infield singled|ground-rule doubled|had catcher's)\b"
)
# GameChanger structure never appears on a PlayMaker page.
_GC_STRUCTURE_RE = re.compile(
    r"(?im)^\s*(?:top|bottom)\s+\d+(?:st|nd|rd|th)\s+-\s+\S|^\s*(?:ball|strike)\s+\d\b|\bin play\."
)


def _label_sentence_pairs(text: str) -> int:
    """Result label lines directly followed by a past-tense play sentence."""
    lines = [" ".join(line.split()) for line in text.splitlines()]
    lines = [line for line in lines if line]
    return sum(
        1
        for label, sentence in zip(lines, lines[1:])
        if _is_label(label) and _PAST_TENSE_PLAY_RE.match(sentence)
    )


def looks_like_playmaker_text(raw_text: str) -> bool:
    """
    PlayMaker page text: result labels each followed by a past-tense play
    sentence ("Fly Out" / "Bowen Cottrill flew out to right field"), or
    'Name #NN' sentences with PlayMaker's runner / fielder markers.
    GameChanger structure vetoes it.
    """
    text = str(raw_text or "")
    if _GC_STRUCTURE_RE.search(text):
        return False
    if _label_sentence_pairs(text) >= 8:
        return True
    return (
        len(_PLAYMAKER_SENTENCE_RE.findall(text)) >= 5
        and len(_PLAYMAKER_MARKER_RE.findall(text)) >= 3
    )


_SCOREBOARD_MARKERS = {"scoreboard", "live streaming", "batting", "scoring summary"}


def _is_end_of_plays(lines: list[str], index: int) -> bool:
    """The scoreboard: 'PFA' / '5' / 'Bottom 7th' (team, score), or its labels."""
    line = lines[index]
    if line.lower() in _SCOREBOARD_MARKERS or line.lower().startswith(("on deck:", "current batter:")):
        return True
    return index + 1 < len(lines) and lines[index + 1].isdigit() and not line.isdigit()


# Positions coaches type into a player's name ("Carlos Cruz 1b walked").
_NAME_POSITION_RE = re.compile(
    r"^([A-ZÀ-Þ][^\n]{0,50}?)\s+(?:1b|2b|3b|ss|lf|cf|rf|dh|picher|pitcher|cacher|catcher)"
    r"(?=\s+(?:grounded|flew|lined|popped|struck|walked|singled|doubled|tripled|homered|"
    r"hit|reached|was|sac|sacrificed|bunted|fouled|infield|ground-rule|had)\b)",
    re.I,
)


def _sentence(line: str) -> str:
    line = _FIELDER_CREDITS_RE.sub("", line)
    line = _JERSEY_SUFFIX_RE.sub("", line).strip()
    return _NAME_POSITION_RE.sub(r"\1", line)


def clean_playmaker_text(raw_text: str) -> list[str]:
    lines = [" ".join(line.split()) for line in str(raw_text or "").splitlines()]
    lines = [line for line in lines if line]

    halves: list[list[str]] = []
    current: list[str] | None = None
    index = 0

    while index < len(lines):
        line = lines[index]

        if _HALF_RE.match(line):
            current = []
            halves.append(current)
            index += 1
            continue

        if current is not None and _is_label(line) and index + 1 < len(lines):
            nxt = lines[index + 1]
            if not _HALF_RE.match(nxt) and not _is_label(nxt):
                block = [line, _sentence(nxt)]
                index += 2
                while index < len(lines) and _CONTINUATION_RE.match(lines[index]):
                    block.append(_sentence(lines[index]))
                    index += 1
                current.append("\n".join(block))
                continue

        # Past the play list (scoreboard, boxes, scoring summary): stop.
        # Lineup notes inside it ("Evan Shin #1 was skipped") are skipped.
        if current is not None and _is_end_of_plays(lines, index):
            break

        index += 1

    blocks: list[str] = []
    for half in reversed(halves):
        blocks.extend(reversed(half))
    return blocks


__all__ = ["clean_playmaker_text", "looks_like_playmaker_text"]
