# Baseball Language Engine (BLE)

The Baseball Language Engine (BLE) is a source-agnostic baseball parsing engine designed to convert play-by-play from multiple baseball platforms into one standardized baseball model.

BLE is the foundation that powers Opponent IQ.

---

# Purpose

BLE is responsible for one job:

Convert baseball language into structured baseball data.

It does **not** generate reports.

It does **not** calculate scouting reports.

It does **not** contain Opponent IQ business logic.

BLE produces a standardized Game object that downstream applications can consume.

---

# Architecture

```
Raw Source
      ↓
Source Detection
      ↓
Cleaner
      ↓
Parser
      ↓
Game Object
      ↓
Stat Aggregators
      ↓
Adapters
      ↓
Applications (Opponent IQ)
```

The parser is completely independent of Opponent IQ.

Opponent IQ is simply one consumer of BLE.

---

# Design Principles

## Source Agnostic

BLE is built so that every supported source follows the same pipeline.

Current supported sources:

- ✅ GameChanger
- ✅ MLB
- ✅ ESPN College
- ✅ iScore

Planned support:

- Playmaker
- StatBroadcast
- NCAA
- AthletesGoLive
- Additional providers

---

## Never Invent Baseball Data

BLE only extracts information that actually exists in the source.

Examples:

If a source provides:

```
Singles to center.
```

BLE extracts:

- Single
- Ball In Play
- Center Field

If a source does **not** provide:

- Pitch sequence
- Hit location
- Runner identity
- Count

BLE leaves those fields empty.

Missing information is never guessed.

---

## Opponent IQ Independence

BLE is not Opponent IQ.

BLE is a reusable baseball parsing engine.

Opponent IQ consumes BLE through adapters that translate BLE's standardized Game model into Opponent IQ statistics and reports.

This separation allows BLE to support additional baseball applications in the future.

---

# Current Capabilities

BLE currently extracts:

- Batter
- Primary event
- Secondary events
- Ball type
- Hit location
- Ball in play
- Runner events
- Stolen bases
- Caught stealing
- Bunt events
- Pitch sequence (when available)

---

# Validation Philosophy

BLE is validated using complete real baseball games.

Validation occurs in layers:

1. Source Detection
2. Cleaner Validation
3. Parser Validation
4. Stat Validation
5. Application Parity

This ensures parser changes are verified using real baseball data rather than isolated sentences.

---

# Current Project Status

## Source Support

| Source | Status |
|---------|--------|
| GameChanger | ✅ Complete |
| MLB | ✅ Complete |
| ESPN College | ✅ Complete |
| iScore | ✅ Complete |

---

## Validation

- ✅ Full GameChanger parity against the legacy Opponent IQ parser
- ✅ MLB validation
- ✅ College validation
- ✅ iScore validation
- ✅ 171 automated tests passing

---

# Developer Tools

BLE includes an inspection framework for debugging and validation.

Current tooling includes:

- Game inspection
- Play inspection
- Report inspection
- Workbench
- Validation suite

These tools provide a consistent workflow for validating existing sources and developing new ones.

---

# Future Roadmap

- Expand the BLE Workbench
- Add validation automation
- Add parser comparison tools
- Integrate BLE into Opponent IQ (shadow mode)
- Transition Opponent IQ to BLE as the production parser
- Add additional baseball sources

---

# License

Private project.

Developed as the parsing engine that powers Opponent IQ.