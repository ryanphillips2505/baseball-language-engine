# Baseball Language Engine

## Event Taxonomy v1

Purpose:

Define every normalized baseball event type recognized by the engine.

These event types are source-agnostic.

GameChanger, MLB, iScore, AthletesGoLive, CSV imports, and future sources should all normalize into these event types.

---

# HIT EVENTS

## SINGLE

Batter awarded a single.

Examples:

- singles on a ground ball
- singles on a line drive
- singles on a bunt

---

## DOUBLE

Batter awarded a double.

Examples:

- doubles on a line drive
- doubles on a fly ball

---

## TRIPLE

Batter awarded a triple.

Examples:

- triples on a line drive
- triples on a fly ball

---

## HOME_RUN

Batter awarded a home run.

Examples:

- homers on a fly ball

---

# OUT EVENTS

## GROUND_OUT

Examples:

- grounds out to shortstop
- grounds out pitcher to first

---

## FLY_OUT

Examples:

- flies out to center field
- flies out in foul territory

---

## LINE_OUT

Examples:

- lines out to shortstop

---

## POP_OUT

Examples:

- pops out to second baseman

---

## INFIELD_FLY

Examples:

- out on infield fly

---

# STRIKEOUT EVENTS

## STRIKEOUT_LOOKING

Examples:

- strikes out looking

---

## STRIKEOUT_SWINGING

Examples:

- strikes out swinging

---

## DROPPED_THIRD_STRIKE_REACH

Examples:

- reaches on dropped 3rd strike

---

## DROPPED_THIRD_STRIKE_OUT

Examples:

- out at first on dropped 3rd strike

---

# REACH EVENTS

## WALK

Examples:

- walks

---

## HIT_BY_PITCH

Examples:

- is hit by pitch

---

## ERROR

Examples:

- reaches on an error

---

# SACRIFICE EVENTS

## SAC_BUNT

Examples:

- sacrifices
- sacrifice bunt

---

## SAC_FLY

Examples:

- out on sacrifice fly

---

# FIELDER'S CHOICE EVENTS

## FIELDERS_CHOICE

Examples:

- grounds into fielder's choice

---

## FC_DOUBLE_PLAY

Examples:

- grounds into a fielder's choice double play
- flies into a fielder's choice double play

---

# DOUBLE PLAY EVENTS

## DOUBLE_PLAY

Examples:

- grounds into a double play
- lines into a double play
- bunts into a double play

---

# BASERUNNING EVENTS

## STOLEN_BASE

Examples:

- steals 2nd
- steals 3rd

---

## CAUGHT_STEALING

Examples:

- caught stealing 2nd
- caught stealing 3rd
- caught stealing home

---

## PICKOFF

Examples:

- picked off at 1st
- picked off at 2nd

---

## RUNNER_OUT

Examples:

- out advancing to home
- out advancing to 2nd

---

# ADVANCEMENT EVENTS

## WILD_PITCH_ADVANCE

Examples:

- advances on wild pitch
- scores on wild pitch

---

## PASSED_BALL_ADVANCE

Examples:

- advances on passed ball
- scores on passed ball

---

# SUBSTITUTION EVENTS

## COURTESY_RUNNER

Examples:

- Courtesy runner ...

---

## PINCH_RUNNER

Examples:

- Pinch runner ...

---

## PITCHING_CHANGE

Examples:

- X in for pitcher Y

---

## LINEUP_CHANGE

Examples:

- Lineup changed ...

---

# FUTURE EVENTS

Reserved for future discovery.

Examples:

- Balk
- Catcher's Interference
- Obstruction
- Appeal Play
- Defensive Indifference
