from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass


_POSITION_SUFFIXES = (
    "PH-1B",
    "PH-2B",
    "PH-3B",
    "PH-SS",
    "PH-LF",
    "PH-CF",
    "PH-RF",
    "PH-C",
    "PH-DH",
    "PH-P",
    "DH-P",
    "P-DH",
    "PH",
    "PR",
    "1B",
    "2B",
    "3B",
    "SS",
    "LF",
    "CF",
    "RF",
    "DH",
    "OF",
    "C",
    "P",
)

# a-/b- pinch-hit markers and 1-/2- pinch-run markers from MLB.com box scores.
_PINCH_PREFIX_RE = re.compile(r"^(?:[a-z]|\d)-")
_BOX_TOKEN_RE = re.compile(
    r"^(?:(?:[a-z]|\d)-)?"
    r"[A-Za-zÀ-ÿ'’. -]+"
    r"(?:,\s*[A-Za-z]+)?"
    r"(?:"
    + "|".join(re.escape(p) for p in _POSITION_SUFFIXES)
    + r")$"
)


@dataclass(frozen=True)
class BoxPlayerRef:
    raw: str
    last_name: str
    initials: str | None
    position: str | None
    pinch_marker: str | None


def _strip_accents(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in normalized if not unicodedata.combining(ch))


def _norm_name(text: str) -> str:
    return re.sub(r"\s+", " ", _strip_accents(text).lower()).strip(" .")


def parse_box_player_token(token: str) -> BoxPlayerRef | None:
    """
    Parse IQ Capture / MLB.com box tokens like:
    - Sogard2B
    - Abreu, WRF
    - Contreras, Wn1B
    - a-CallPH-RF
    - b-Hernández, EPH-1B
    """

    text = " ".join(str(token or "").split()).strip()
    if not text or not _BOX_TOKEN_RE.match(text):
        return None

    pinch_marker = None
    prefix = _PINCH_PREFIX_RE.match(text)
    if prefix:
        pinch_marker = prefix.group(0)[0]
        text = text[prefix.end() :]

    position = None
    for suffix in _POSITION_SUFFIXES:
        if text.endswith(suffix):
            # Avoid stripping a lone trailing C/P that is part of a short last name
            # only when a position-looking suffix remains after a name body.
            body = text[: -len(suffix)]
            if not body:
                continue
            position = suffix
            text = body
            break

    if not text:
        return None

    initials = None
    if "," in text:
        last_name, _, rest = text.partition(",")
        last_name = last_name.strip()
        initials = rest.strip() or None
    else:
        last_name = text.strip()

    if not last_name:
        return None

    return BoxPlayerRef(
        raw=token,
        last_name=last_name,
        initials=initials,
        position=position,
        pinch_marker=pinch_marker,
    )


def _split_full_name(full_name: str) -> tuple[str, str]:
    parts = full_name.strip().split()
    if not parts:
        return "", ""
    if len(parts) == 1:
        return "", parts[0]
    return " ".join(parts[:-1]), parts[-1]


def _initials_match(initials: str, first_name: str) -> bool:
    init = _norm_name(initials).replace(".", "").replace(" ", "")
    first = _norm_name(first_name).replace("-", "").replace(" ", "")
    if not init or not first:
        return False
    if first.startswith(init):
        return True
    # Box abbreviations sometimes keep an extra letter ("Wn" for Willson).
    return first[0] == init[0]


def match_box_ref_to_full_name(
    box_ref: BoxPlayerRef,
    full_names: list[str],
) -> str | None:
    last = _norm_name(box_ref.last_name)
    candidates: list[str] = []
    for full in full_names:
        first, family = _split_full_name(full)
        if _norm_name(family) != last:
            continue
        if box_ref.initials:
            if not _initials_match(box_ref.initials, first):
                continue
        candidates.append(full)

    if len(candidates) == 1:
        return candidates[0]
    if len(candidates) > 1 and box_ref.initials:
        # Prefer the tightest first-name prefix match.
        init = _norm_name(box_ref.initials).replace(".", "")
        ranked = sorted(
            candidates,
            key=lambda name: (
                0
                if _norm_name(_split_full_name(name)[0]).startswith(init)
                else 1,
                len(name),
            ),
        )
        return ranked[0]
    if len(candidates) > 1:
        return None
    return None


def map_box_tokens_to_full_names(
    box_tokens: list[str],
    full_names: list[str],
) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for token in box_tokens:
        ref = parse_box_player_token(token)
        if ref is None:
            continue
        full = match_box_ref_to_full_name(ref, full_names)
        if full:
            mapping[token] = full
    return mapping


__all__ = [
    "BoxPlayerRef",
    "parse_box_player_token",
    "match_box_ref_to_full_name",
    "map_box_tokens_to_full_names",
]
