from aggregators.game_stat_aggregator import aggregate_game_stats
from aggregators.swing_decision_aggregator import aggregate_swing_decisions
from models.game import Game

from .game_inspector import build_game_inspection
from .models import GameInspection, PlayInspection
from .play_inspector import build_play_inspection


class Workbench:
    def inspect_play(self, raw_play: str) -> PlayInspection:
        return build_play_inspection(raw_play)

    def inspect_game(self, raw_plays: list[str]) -> GameInspection:
        return build_game_inspection(raw_plays)