from __future__ import annotations

from assemblers.pitch_decision_builder import build_pitch_decisions
from assemblers.plate_appearance_builder import build_plate_appearance
from cleaners.gamechanger_cleaner import normalize_pbp, _BASEBALL_ACTION_RE, _PITCH_TOKEN_RE
from extractors.pitch_token_extractor import extract_pitch_tokens
from models.game import Game


def build_gamechanger_swing_game(raw_text: str) -> Game:
    lines = normalize_pbp(raw_text)

    plate_appearances = []
    pending_pitch_lines: list[str] = []

    for line in lines:
        has_pitch = bool(_PITCH_TOKEN_RE.search(line))
        has_action = bool(_BASEBALL_ACTION_RE.search(line))

        if has_pitch and not has_action:
            pending_pitch_lines.append(line)
            continue

        if has_action:
            pa = build_plate_appearance(line)

            if pending_pitch_lines:
                pitch_tokens = extract_pitch_tokens(pending_pitch_lines)
                pa.pitches = build_pitch_decisions(pitch_tokens)
                pending_pitch_lines = []

            plate_appearances.append(pa)

    return Game(plate_appearances=plate_appearances)


__all__ = [
    "build_gamechanger_swing_game",
]