from __future__ import annotations

from enum import Enum


class EventType(str, Enum):
    SINGLE = "single"
    DOUBLE = "double"
    TRIPLE = "triple"
    HOME_RUN = "home_run"

    GROUND_OUT = "ground_out"
    FLY_OUT = "fly_out"
    LINE_OUT = "line_out"
    POP_OUT = "pop_out"
    INFIELD_FLY = "infield_fly"

    STRIKEOUT_LOOKING = "strikeout_looking"
    STRIKEOUT_SWINGING = "strikeout_swinging"

    DROPPED_THIRD_STRIKE_REACH = "dropped_third_strike_reach"
    DROPPED_THIRD_STRIKE_OUT = "dropped_third_strike_out"

    WALK = "walk"
    INTENTIONAL_WALK = "intentional_walk"
    HIT_BY_PITCH = "hit_by_pitch"
    ERROR = "error"

    SAC_BUNT = "sac_bunt"
    SAC_FLY = "sac_fly"

    FIELDERS_CHOICE = "fielders_choice"
    FC_DOUBLE_PLAY = "fc_double_play"

    DOUBLE_PLAY = "double_play"

    STOLEN_BASE = "stolen_base"
    CAUGHT_STEALING = "caught_stealing"
    PICKOFF = "pickoff"
    RUNNER_OUT = "runner_out"

    WILD_PITCH_ADVANCE = "wild_pitch_advance"
    PASSED_BALL_ADVANCE = "passed_ball_advance"

    COURTESY_RUNNER = "courtesy_runner"
    PINCH_RUNNER = "pinch_runner"
    PITCHING_CHANGE = "pitching_change"
    LINEUP_CHANGE = "lineup_change"
