# Detection Strategy v1

## Purpose

Define how the Baseball Language Engine identifies events inside a PA block.

No parser code should be written until event detection rules are documented.

---

# Detection Flow

PA Block
↓
Identify Candidate Events
↓
Classify Event Types
↓
Normalize Events
↓
Structured Output

---

# HIT DETECTION

## SINGLE

Language Patterns

- singles on a ground ball
- singles on a line drive
- singles on a bunt

Output

- EventType.SINGLE

---

## DOUBLE

Language Patterns

- doubles on a line drive
- doubles on a fly ball

Output

- EventType.DOUBLE

---

## TRIPLE

Language Patterns

- triples on a line drive
- triples on a fly ball

Output

- EventType.TRIPLE

---

## HOME RUN

Language Patterns

- homers on a fly ball
- homers to left field
- homers to center field
- homers to right field

Output

- EventType.HOME_RUN

---

# OUT DETECTION

## GROUND OUT

Language Patterns

- grounds out

Output

- EventType.GROUND_OUT

---

## FLY OUT

Language Patterns

- flies out

Output

- EventType.FLY_OUT

---

## LINE OUT

Language Patterns

- lines out

Output

- EventType.LINE_OUT

---

## POP OUT

Language Patterns

- pops out

Output

- EventType.POP_OUT

---

## INFIELD FLY

Language Patterns

- out on infield fly

Output

- EventType.INFIELD_FLY

---

# STRIKEOUT DETECTION

## STRIKEOUT LOOKING

Language Patterns

- strikes out looking

Output

- EventType.STRIKEOUT_LOOKING

---

## STRIKEOUT SWINGING

Language Patterns

- strikes out swinging

Output

- EventType.STRIKEOUT_SWINGING

---

## DROPPED THIRD STRIKE REACH

Language Patterns

- reaches on dropped 3rd strike

Output

- EventType.DROPPED_THIRD_STRIKE_REACH

---

## DROPPED THIRD STRIKE OUT

Language Patterns

- out at first on dropped 3rd strike

Output

- EventType.DROPPED_THIRD_STRIKE_OUT

---

# REACH DETECTION

## WALK

Language Patterns

- walks

Output

- EventType.WALK

---

## HIT BY PITCH

Language Patterns

- is hit by pitch

Output

- EventType.HIT_BY_PITCH

---

## ERROR

Language Patterns

- reaches on an error

Output

- EventType.ERROR

---

# IMPORTANT RULE

A PA may generate multiple events.

Example:

Runner steals 2nd.
Runner scores on wild pitch.
Batter walks.

Detected Events:

- STOLEN_BASE
- WILD_PITCH_ADVANCE
- WALK

The engine must not assume a PA contains only one event.
