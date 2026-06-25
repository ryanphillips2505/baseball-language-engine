from dataclasses import dataclass
from typing import Any

from models.game import Game


@dataclass
class PlayInspection:
    raw_play: str
    lines: list[str]
    result_line: str
    plate_appearance: Any
    pitch_tokens: list[Any]
    pitch_decisions: list[Any]
    stat_changes: dict[str, int]


@dataclass
class ReportInspection:
    season_summary_rows: list[dict[str, Any]]
    spray_zone_rows: list[dict[str, Any]]
    damage_rows: list[dict[str, Any]]
    swing_decision_rows: list[dict[str, Any]]
    player_cards: list[dict[str, Any]]


@dataclass
class GameInspection:
    raw_plays: list[str]
    play_inspections: list[PlayInspection]
    game: Game
    game_stats: dict[str, dict[str, Any]]
    swing_stats: dict[str, dict[str, dict[str, int]]]
    reports: ReportInspection