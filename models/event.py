from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class BaseballEvent:
    player: str
    raw_text: str

    source: str = "unknown"

    # Core batter result
    result: Optional[str] = None          # OUT, 1B, 2B, 3B, HR, BB, HBP, ROE, FC, K, SAC, UNKNOWN
    is_bip: bool = False

    # Contact profile
    ball_type: Optional[str] = None       # GB, FB, LD, PU, BUNT, UNKNOWN
    location: Optional[str] = None        # LF, CF, RF, 3B, SS, 2B, 1B, P, C, UNKNOWN

    # Production
    rbi: int = 0
    runs_scored: int = 0

    # Baserunning
    stolen_bases: int = 0
    caught_stealing: int = 0
    sb_runners: list[str] = field(default_factory=list)
    cs_runners: list[str] = field(default_factory=list)

    # Bunt / XBH
    bunt: bool = False
    sac_bunt: bool = False
    xbh: Optional[str] = None             # 2B, 3B, HR
    xbh_loc: Optional[str] = None         # XBH_LF, XBH_CF, XBH_RF, XBH_UNKNOWN

    # Special events
    d3k_reach: bool = False
    foul_tip_k: bool = False
    intentional_walk: bool = False
    fc_double_play: bool = False
    lines_into_double_play: bool = False
    flies_into_double_play: bool = False
    bunt_double_play: bool = False

    # Parser confidence / notes
    confidence: float = 1.0
    warnings: list[str] = field(default_factory=list)
