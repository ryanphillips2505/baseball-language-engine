from typing import Any

from aggregators.game_stat_aggregator import aggregate_game_stats
from assemblers.pitch_decision_builder import build_pitch_decisions
from assemblers.plate_appearance_builder import build_plate_appearance
from extractors.pitch_token_extractor import extract_pitch_tokens
from models.game import Game

from .constants import STAT_DISPLAY_ORDER
from .models import PlayInspection


def clean_lines(raw_play: str) -> list[str]:
    return [
        line.strip()
        for line in raw_play.splitlines()
        if line.strip()
    ]


def get_result_line(raw_play: str, lines: list[str]) -> str:
    return lines[-1] if lines else raw_play.strip()


def build_stat_changes(pa: Any) -> dict[str, int]:
    game = Game(plate_appearances=[pa])
    stats = aggregate_game_stats(game)

    player = pa.batter_name

    if not player and pa.runner_events:
        for runner_event in pa.runner_events:
            if runner_event.runner_name in stats:
                player = runner_event.runner_name
                break

    if not player or player not in stats:
        return {}

    player_stats = stats[player]
    changes: dict[str, int] = {}

    for key in STAT_DISPLAY_ORDER:
        value = int(player_stats.get(key, 0) or 0)

        if key == "GP":
            continue

        if value:
            changes[key] = value

    return changes


def build_play_inspection(raw_play: str) -> PlayInspection:
    lines = clean_lines(raw_play)
    result_line = get_result_line(raw_play, lines)

    pa = build_plate_appearance(result_line)

    pitch_tokens = extract_pitch_tokens(lines)
    pitch_decisions = build_pitch_decisions(pitch_tokens)

    pa.pitches = pitch_decisions

    stat_changes = build_stat_changes(pa)

    return PlayInspection(
        raw_play=raw_play,
        lines=lines,
        result_line=result_line,
        plate_appearance=pa,
        pitch_tokens=pitch_tokens,
        pitch_decisions=pitch_decisions,
        stat_changes=stat_changes,
    )