# Architecture Decision #1

## Question

Should one Plate Appearance (PA) block create exactly one BaseballEvent?

Example:

Ball 1, Runner steals 2nd, Ball 2, Runner scores on wild pitch, Ball 3, Ball 4.

Batter walks.

---

## Decision

NO.

A PA block may contain multiple baseball events.

A PA block is a container.

A BaseballEvent is an event that occurred during the PA.

---

# Why

Examples from the corpus:

### Example 1

Runner steals 2nd.

Batter strikes out.

Events:

- Stolen Base
- Strikeout

---

### Example 2

Runner caught stealing.

Batter walks.

Events:

- Caught Stealing
- Walk

---

### Example 3

Runner scores on wild pitch.

Batter reaches on error.

Events:

- Wild Pitch Advance
- Run Scored
- Error

---

### Example 4

Pinch runner enters.

Runner steals 2nd.

Batter grounds out.

Events:

- Pinch Runner
- Stolen Base
- Ground Out

---

# Important Concept

PA Block ≠ Baseball Event

A PA block is a collection of baseball language.

The language engine should first identify all baseball events contained within the block.

Only after identification should events be normalized.

---

# Future Architecture

Raw PA Block
↓
Event Detection
↓
Detected Events
↓
Normalization
↓
BaseballEvent Objects

Example:

PA Block
↓
[
    StolenBase,
    WildPitchAdvance,
    Walk
]
↓
Normalized Events
↓
Structured Output

---

# Implication

The current BaseballEvent model should be viewed as a normalized output model.

It should NOT dictate how the language engine processes a PA block.

The language engine should remain free to detect multiple events inside a single PA.
