from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Iterator

from models.timeline_block import TimelineBlock, TimelineBlockType


@dataclass
class Timeline:
    blocks: list[TimelineBlock] = field(default_factory=list)

    def append(self, block: TimelineBlock) -> None:
        self.blocks.append(block)

    def extend(self, blocks: Iterable[TimelineBlock]) -> None:
        self.blocks.extend(blocks)

    def __iter__(self) -> Iterator[TimelineBlock]:
        return iter(self.blocks)

    def __len__(self) -> int:
        return len(self.blocks)

    def plate_appearance_blocks(self) -> list[TimelineBlock]:
        return [
            block for block in self.blocks
            if block.block_type == TimelineBlockType.PLATE_APPEARANCE
        ]

    def game_event_blocks(self) -> list[TimelineBlock]:
        return [
            block for block in self.blocks
            if block.block_type == TimelineBlockType.GAME_EVENT
        ]
