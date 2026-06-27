from __future__ import annotations

from cleaners.gamechanger_cleaner import _BASEBALL_ACTION_RE, _PITCH_TOKEN_RE


def group_gamechanger_plate_appearances(lines: list[str]) -> list[str]:
    plate_appearances: list[str] = []
    pending_pitch_lines: list[str] = []

    for line in lines:
        has_pitch = bool(_PITCH_TOKEN_RE.search(line))
        has_action = bool(_BASEBALL_ACTION_RE.search(line))

        if has_pitch and not has_action:
            pending_pitch_lines.append(line)
            continue

        if has_action:
            if pending_pitch_lines:
                plate_appearances.append(
                    "\n".join([*pending_pitch_lines, line])
                )
                pending_pitch_lines = []
            else:
                plate_appearances.append(line)

    return plate_appearances


__all__ = [
    "group_gamechanger_plate_appearances",
]