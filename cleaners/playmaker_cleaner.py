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


def looks_like_playmaker_text(raw_text: str) -> bool:
    """PlayMaker page text: past-tense 'Name #NN' sentences plus its markers."""
    text = str(raw_text or "")
    return (
        len(_PLAYMAKER_SENTENCE_RE.findall(text)) >= 5
        and len(_PLAYMAKER_MARKER_RE.findall(text)) >= 3
    )


def _sentence(line: str) -> str:
    line = _FIELDER_CREDITS_RE.sub("", line)
    return _JERSEY_SUFFIX_RE.sub("", line).strip()


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
        if current is not None and any(halves):
            break

        index += 1

    blocks: list[str] = []
    for half in reversed(halves):
        blocks.extend(reversed(half))
    return blocks


__all__ = ["clean_playmaker_text", "looks_like_playmaker_text"]
