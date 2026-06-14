from __future__ import annotations


def is_ball_in_play(
    ball_type: str | None,
) -> bool:
    return ball_type in {
        "GB",
        "FB",
        "BUNT",
    }
