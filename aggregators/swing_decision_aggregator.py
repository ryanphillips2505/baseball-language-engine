from __future__ import annotations

from collections import defaultdict

from models.game import Game
from models.pitch_decision import PitchOutcome


COUNT_ORDER = [
    "0-0",
    "1-0",
    "0-1",
    "2-0",
    "1-1",
    "0-2",
    "3-0",
    "2-1",
    "1-2",
    "3-1",
    "2-2",
    "3-2",
]


def _empty_count_bucket() -> dict[str, int]:
    return {
        "PA": 0,
        "BIP": 0,
        "SWING_MISS": 0,
        "FOUL": 0,
        "CALLED_STRIKE": 0,
        "BALL": 0,
    }


def _empty_player_map() -> dict[str, dict[str, int]]:
    return {count: _empty_count_bucket() for count in COUNT_ORDER}


def aggregate_swing_decisions(
    game: Game,
) -> dict[str, dict[str, dict[str, int]]]:
    totals: dict[str, dict[str, dict[str, int]]] = defaultdict(_empty_player_map)

    for pa in game.plate_appearances:
        player = str(pa.batter_name or "").strip()

        if not player:
            continue

        reached_counts: set[str] = set()

        for pitch in pa.pitches:
            count = str(pitch.count)

            if count not in COUNT_ORDER:
                continue

            reached_counts.add(count)

            if pitch.outcome == PitchOutcome.BIP:
                totals[player][count]["BIP"] += 1
            elif pitch.outcome == PitchOutcome.SWING_MISS:
                totals[player][count]["SWING_MISS"] += 1
            elif pitch.outcome == PitchOutcome.FOUL:
                totals[player][count]["FOUL"] += 1
            elif pitch.outcome == PitchOutcome.CALLED_STRIKE:
                totals[player][count]["CALLED_STRIKE"] += 1
            elif pitch.outcome == PitchOutcome.BALL:
                totals[player][count]["BALL"] += 1

        for count in reached_counts:
            totals[player][count]["PA"] += 1

    return dict(totals)


__all__ = [
    "COUNT_ORDER",
    "aggregate_swing_decisions",
]