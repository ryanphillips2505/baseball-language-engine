"""
Multi-platform play-by-play language support.

GameChanger is read by the legacy BLE path, which is frozen to match
the production Opponent IQ GameChanger reading. Every other platform
(MLB Gameday, ESPN, StatCrew-family college feeds, iScore, ...) is read
through this package:

    normalizer   rewrites platform vocabulary aliases (position
                 abbreviations, direction phrases, review prefixes)
                 into BLE's canonical wording
    reader       reads one plate appearance with the legacy detectors
                 plus the extra phrasings other platforms use

Nothing in this package is used for GameChanger.
"""

from language.reader import build_multi_platform_plate_appearance

__all__ = [
    "build_multi_platform_plate_appearance",
]
