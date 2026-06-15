from __future__ import annotations

from dataclasses import dataclass, field

from models.plate_appearance import PlateAppearance


@dataclass
class Game:
    plate_appearances: list[PlateAppearance] = field(default_factory=list)

    def players_in_game(self) -> set[str]:
        players: set[str] = set()

        for pa in self.plate_appearances:
            if pa.batter_name:
                players.add(pa.batter_name)

            for runner_event in pa.runner_events:
                if runner_event.runner_name:
                    players.add(runner_event.runner_name)

        return players