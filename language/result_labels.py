"""
Result labels that scoring apps print above a play's sentence.

PlayMaker shows each play as a result label ("Ground Out", "Bunt,
Reached on Error") followed by a sentence from its server. The labels
below are PlayMaker's complete list, taken from its web app's own
result-code table (play.playmakerapp.io, Oct 2026). The sentence
wording has not been verified yet, so the reader uses a label only when
it cannot read the sentence itself.

Each label maps to (EventType, ball type or None). A ball type is set
only where the label itself says how the ball was hit.
"""

from __future__ import annotations

from models.types import EventType


PLAYMAKER_RESULT_LABELS: dict[str, tuple[EventType, str | None]] = {
    "single": (EventType.SINGLE, None),
    "double": (EventType.DOUBLE, None),
    "ground rule double": (EventType.DOUBLE, None),
    "triple": (EventType.TRIPLE, None),
    "home run": (EventType.HOME_RUN, None),
    "ground out": (EventType.GROUND_OUT, "GB"),
    "hard ground out": (EventType.GROUND_OUT, "GB"),
    "line out": (EventType.LINE_OUT, "FB"),
    "fly out": (EventType.FLY_OUT, "FB"),
    "foul out": (EventType.POP_OUT, "FB"),
    "out": (EventType.FIELD_OUT, None),
    "reached on error": (EventType.ERROR, None),
    "strikeout looking": (EventType.STRIKEOUT_LOOKING, None),
    "strike out": (EventType.STRIKEOUT, None),
    "walk": (EventType.WALK, None),
    "intentional walk": (EventType.INTENTIONAL_WALK, None),
    "hit by pitch": (EventType.HIT_BY_PITCH, None),
    "catcher's interference": (EventType.CATCHER_INTERFERENCE, None),
    "fielder's choice": (EventType.FIELDERS_CHOICE, None),
    "fielder's choice (error)": (EventType.FIELDERS_CHOICE, None),
    "double play": (EventType.DOUBLE_PLAY, None),
    "triple play": (EventType.DOUBLE_PLAY, None),
    "sacrifice fly": (EventType.SAC_FLY, "FB"),
    "sacrifice bunt": (EventType.SAC_BUNT, "BUNT"),
    "bunt single": (EventType.SINGLE, "BUNT"),
    "bunt popout": (EventType.POP_OUT, "BUNT"),
    "bunt out": (EventType.FIELD_OUT, "BUNT"),
    "bunt, reached on error": (EventType.ERROR, "BUNT"),
    "dropped 3rd strike, out": (EventType.DROPPED_THIRD_STRIKE_OUT, None),
    "dropped 3rd strike, safe": (EventType.DROPPED_THIRD_STRIKE_REACH, None),
    "dropped 3rd strike, error": (EventType.DROPPED_THIRD_STRIKE_REACH, None),
    "stolen base": (EventType.STOLEN_BASE, None),
    "caught stealing": (EventType.CAUGHT_STEALING, None),
}

# PlayMaker also has a plain "Bunt" label. It does not say whether the
# batter was out or safe, so it is not mapped to an outcome.


def result_label(line: str) -> tuple[EventType, str | None] | None:
    return PLAYMAKER_RESULT_LABELS.get(" ".join(str(line or "").lower().split()))


__all__ = [
    "PLAYMAKER_RESULT_LABELS",
    "result_label",
]
