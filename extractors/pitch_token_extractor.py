from __future__ import annotations

import re


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
    r"In play)",
    re.IGNORECASE,
)


def extract_pitch_tokens(block_lines: list[str]) -> list[str]:
    tokens: list[str] = []

    for line in block_lines:
        raw = str(line or "").strip()
        if not raw:
            continue

        parts = re.split(r",", raw)

        for part in parts:
            piece = part.strip()
            if not piece:
                continue

            match = _PITCH_TOKEN_RE.search(piece)
            if not match:
                continue

            token = re.sub(r"\s+", " ", str(match.group(0)).strip())

            if token:
                tokens.append(token)

    return tokens


__all__ = [
    "extract_pitch_tokens",
]