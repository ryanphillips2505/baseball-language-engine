from __future__ import annotations

from assemblers.game_event_builder import build_game_event
from assemblers.plate_appearance_builder import build_plate_appearance
from assemblers.timeline_builder import build_timeline
from models.game import Game
from models.pitch_event import PitchEvent
from models.plate_appearance_block import PlateAppearanceBlock
from models.timeline_block import (
    GameEventBlock,
    PlateAppearanceBlock as TimelinePlateAppearanceBlock,
    TimelineBlock,
)


def _text_from_legacy_pa_block(block: PlateAppearanceBlock) -> str:
    return "\n".join(
        [
            *block.pitch_lines,
            block.action_text,
        ]
    )


def build_game(
    pa_blocks: list[str] | list[PlateAppearanceBlock] | list[TimelineBlock],
) -> Game:

    plate_appearances = []
    pitch_events: list[PitchEvent] = []

    for block in pa_blocks:
        metadata_pitches = None
        if hasattr(block, "metadata") and isinstance(block.metadata, dict):
            maybe_pitches = block.metadata.get("statsapi_pitches")
            if isinstance(maybe_pitches, list):
                metadata_pitches = [
                    pitch for pitch in maybe_pitches if isinstance(pitch, PitchEvent)
                ]
                pitch_events.extend(metadata_pitches)

        if isinstance(block, GameEventBlock):
            continue

        statsapi_pitches = None

        if isinstance(block, TimelinePlateAppearanceBlock):
            text = block.raw_text
            statsapi_pitches = metadata_pitches

        elif isinstance(block, PlateAppearanceBlock):
            text = _text_from_legacy_pa_block(block)

        else:
            text = block

        plate_appearances.append(
            build_plate_appearance(
                text,
                pitches=statsapi_pitches,
            )
        )

    game = Game(
        plate_appearances=plate_appearances,
        pitch_events=pitch_events,
    )

    game.timeline = build_timeline(
        pa_blocks
    )

    for block in game.timeline.blocks:
        if isinstance(block, GameEventBlock):
            game_event = build_game_event(block)
            block.metadata["game_event"] = game_event

    return game


__all__ = [
    "build_game",
]
