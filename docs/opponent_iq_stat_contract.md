# Opponent IQ Stat Contract

This document defines how Baseball Language Engine outputs must map to Opponent IQ export stats.

Rule: if Baseball Language Engine disagrees with current Opponent IQ exports, Opponent IQ wins.

  ## Core Opponent IQ Batting Stats

### Hits

SINGLE
DOUBLE
TRIPLE
HOME_RUN

### Reach Events

WALK
HIT_BY_PITCH
ERROR
FIELDERS_CHOICE

### Outs

GROUND_OUT
FLY_OUT
LINE_OUT
POP_OUT
INFIELD_FLY

### Special Outs

DOUBLE_PLAY
FC_DOUBLE_PLAY
DROPPED_THIRD_STRIKE_OUT

### Baserunning

STOLEN_BASE
CAUGHT_STEALING
PICKOFF
RUNNER_OUT

### Small Ball

BUNT
SAC_BUNT
SAC_FLY

  ## Derived Opponent IQ Metrics

BIP
GB
FB
BUNT
GB%
FB%
XBH
SB
CS
AVG
SLG
OPS

  ## EventType → Opponent IQ Mapping

| EventType | Opponent IQ Stat |
|------------|------------------|
| SINGLE | 1B |
| DOUBLE | 2B |
| TRIPLE | 3B |
| HOME_RUN | HR |
| WALK | BB |
| HIT_BY_PITCH | HBP |
| STRIKEOUT_LOOKING | K |
| STRIKEOUT_SWINGING | K |
| STOLEN_BASE | SB |
| CAUGHT_STEALING | CS |

## Requires Existing Opponent IQ Logic

These EventTypes cannot be converted directly into final stats without using the existing Opponent IQ pattern engine.

- GROUND_OUT
- FLY_OUT
- LINE_OUT
- POP_OUT
- INFIELD_FLY
- SAC_BUNT
- SAC_FLY
- DOUBLE_PLAY
- FC_DOUBLE_PLAY
- ERROR
- FIELDERS_CHOICE

## Phase 5C Goals

The Baseball Language Engine must eventually produce the same player totals as Opponent IQ.

Validation rule:

Baseball Language Engine Player Stats
=
Opponent IQ Export Stats

If totals disagree:

Opponent IQ wins.

No stat engine should be considered complete until it matches known Opponent IQ exports.

## Future Validation Dataset

Required validation targets:

- Season Summary Export
- Damage Report Export
- Player Card Export
- Excel Workbook Export

Future process:

Raw Text
↓
Cleaner
↓
Detector
↓
Player Extractor
↓
BaseballEvent
↓
Stat Engine
↓
Player Totals

Compare

Player Totals
↓
Opponent IQ Export Totals

Must Match
## Direct EventType Stats

These stats can be calculated directly from BaseballEvent.

SINGLE -> 1B
DOUBLE -> 2B
TRIPLE -> 3B
HOME_RUN -> HR
WALK -> BB
HIT_BY_PITCH -> HBP
STRIKEOUT_LOOKING -> K
STRIKEOUT_SWINGING -> K
STOLEN_BASE -> SB
CAUGHT_STEALING -> CS

These require no additional Opponent IQ pattern logic.

  ## Context Required Stats

These stats require additional information beyond EventType.

BIP
GB
FB
BUNT
GB%
FB%
XBH Location
Spray Chart Location
Damage Metrics
Hard Contact Metrics

These rely on Opponent IQ pattern detection and location classification.

## Future PlateAppearance Model

A PlateAppearance represents a single completed batting event.

class PlateAppearance:

    batter_name

    baseball_event

    ball_type
        GB
        FB
        BUNT

    location
        LF
        CF
        RF
        3B
        SS
        2B
        1B
        P

    xbh_type

    xbh_location

    runner_events  

## Swing Decision Layer

Swing Decisions are not determined from EventType alone.

Swing Decisions require pitch-level context:

- Count
- Pitch number
- Ball / Strike result
- Swing / Take
- Foul
- Ball in play
- Strikeout pitch
- Walk pitch

Future Swing Decision outputs must match the existing Opponent IQ Swing Decision PDF.

Rule:

Baseball Language Engine Swing Decision totals are not correct unless they match Opponent IQ Swing Decision exports.
