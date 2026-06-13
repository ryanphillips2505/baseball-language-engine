# Baseball Language Engine

## Purpose

Convert baseball play-by-play language from any source into a normalized event structure.

Examples of supported future sources:

- GameChanger
- MLB
- iScore
- AthletesGoLive
- CSV exports
- Manual scorekeeping systems

Pipeline:

Raw Source
↓
Translator
↓
Normalized Event
↓
Reports / Analytics

---

# Event Families

## HIT

Events where the batter records a hit.

- Single
- Double
- Triple
- Home Run

---

## OUT

Events where the batter is retired.

- Ground Out
- Fly Out
- Line Out
- Pop Out
- Infield Fly

---

## STRIKEOUT

Strikeout outcomes.

- Strikeout Looking
- Strikeout Swinging

Special cases:

- Dropped Third Strike Reach
- Dropped Third Strike Out

---

## REACH

Events where the batter reaches safely without a hit.

- Walk
- Hit By Pitch
- Error
- Dropped Third Strike Reach

---

## SACRIFICE

Intentional advancement plays.

- Sacrifice Bunt
- Sacrifice Fly

---

## FIELDER'S CHOICE

Batter reaches or runner retired via fielder's choice.

- Fielder's Choice
- FC Double Play

---

## DOUBLE PLAY

Double play events.

- Ground Ball Double Play
- Line Drive Double Play
- Fly Ball Double Play
- Bunt Double Play

---

## BASERUNNING

Runner events occurring during a plate appearance.

- Stolen Base
- Caught Stealing
- Pickoff
- Runner Out
- Wild Pitch Advance
- Passed Ball Advance

---

## SUBSTITUTIONS

Roster changes occurring during a plate appearance.

- Courtesy Runner
- Pinch Runner
- Pitching Change
- Lineup Change

---

# Important Design Rule

A plate appearance may contain multiple baseball events.

Example:

- Stolen Base
- Wild Pitch
- Runner Advancement
- Walk

All may occur inside the same PA block.

The PA result is not necessarily the only event.

The engine must separate:

1. Batter Result
2. Runner Events
3. Substitution Events
4. Defensive Events

before creating a normalized event.
