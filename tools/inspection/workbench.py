from .game_inspector import build_game_inspection
from .models import GameInspection, PlayInspection
from .play_inspector import build_play_inspection
from .printers import print_game_inspection, print_play_inspection


class Workbench:
    def inspect_play(self, raw_play: str) -> PlayInspection:
        return build_play_inspection(raw_play)

    def inspect_game(self, raw_plays: list[str]) -> GameInspection:
        return build_game_inspection(raw_plays)

    def print_play(self, inspection: PlayInspection) -> None:
        print_play_inspection(inspection)

    def print_game(self, inspection: GameInspection) -> None:
        print_game_inspection(inspection)