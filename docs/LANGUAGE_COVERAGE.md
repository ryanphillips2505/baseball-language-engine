# Multi-Platform Language Coverage

Goal: read every platform's play-by-play language into Opponent IQ
stats, without changing what Opponent IQ reads from GameChanger.

## How it is wired

```
raw text -> detect_source -> platform cleaner
   GameChanger  -> legacy reader (frozen)            -> Game
   everything else -> language/normalizer + language/reader -> Game
```

- `pipeline/process_game.py` sends GameChanger to the legacy reader
  exactly as before and every other source to
  `language.reader.build_multi_platform_plate_appearance`.
- `tests/test_frozen_source_outputs.py` freezes the full GameChanger
  reading (every plate appearance, game events, aggregate stats, final
  Opponent IQ stats) for all GameChanger samples. Any GameChanger change
  fails it. Regenerate only on purpose: `py -m tools.output_snapshot write`.

## Platform families covered

| Family | Who writes it | Example |
|---|---|---|
| GameChanger | GC (HS / youth) | `C Cunningham lines out to shortstop E Fish.` (legacy, frozen) |
| MLB Gameday | MLB.com, MiLB | `Sam Ortiz grounds out, pitcher Lee Park to first baseman Bo Hart.` |
| ESPN generated | ESPN MLB + college | `S. Ortiz grounded into fielder's choice to shortstop, A. Cole out at second.` |
| StatCrew family | NCAA stats, Sidearm, PrestoSports, StatBroadcast, ESPN college feeds | `Ortiz grounded out to ss (1-2 KBK).` |
| iScore | iScore | `#7 Sam Ortiz hits a medium line drive for a single.` |

StatCrew pitch codes `(count SEQUENCE)` become swing decisions
(B ball, K called strike, S swinging strike, F foul; in-play pitch
added for balls in play). Unknown codes are not guessed.

## Measured results (local research corpus, Oct 2026)

Language audit (`tools/language_audit/audit.py`) on harvested plays:

| Corpus | Plays | Read cleanly |
|---|---|---|
| MLB Stats API (152 games) | 11,614 | 99.8% (scored against MLB event / trajectory / fielder truth) |
| MiLB | 2,517 | 99.7% |
| ESPN MLB | 2,719 | 99.9% |
| ESPN college (488 games) | 13,764 | 99.6% (2,644 ESPN-labelled plays: 4 disagreements, all ESPN label noise) |

End to end (`tools/language_audit/boxscore_parity.py`): 89 MLB games
rebuilt from play-by-play, run through `process_game`, compared with
official box scores for K, BB, HBP, 2B, 3B, HR, SB, CS, BIP:
**16,119 player-stat checks, 99.988% match** (2 misses, both feed data
quirks).

Before this work the same college corpus read cleanly 54% of the time
and ESPN MLB 77%.

## Reading rules (non-GameChanger)

- Never invent: ball type only when the text says how the ball was hit.
- Location comes from the batter's own clause, never runner clauses.
- K / BB / HBP / catcher's interference carry no location.
- Pitcher-started plays credit the pitcher (`grounds out, pitcher X to
  first baseman Y` -> P). GameChanger keeps its legacy behaviour (1B).
- Direction phrases map to a field: up the middle -> CF, through the
  left side -> LF, through the right side -> RF, down the lf/rf line ->
  LF/RF. No ball type is inferred from them.
- On a force play with no fielder in the batter clause, the first
  fielder of the force chain (`out at second ss to 2b`) is the location.
- Generic outcomes: `struck out` (no type) -> STRIKEOUT (counts K),
  `out at first 1b to p` -> FIELD_OUT (BIP, no ball type).
- Line drives count as FB, as in Opponent IQ.

## Tools

| Command | What it does |
|---|---|
| `py -m tools.language_audit.harvest_mlb_statsapi out.jsonl 1 2025-06-14` | Harvest MLB plays + truth labels |
| `py -m tools.language_audit.harvest_espn out.jsonl college-baseball 20250315` | Harvest ESPN plays + labels |
| `py -m tools.language_audit.audit out.jsonl mlb_statsapi report.md` | Misreads grouped by phrasing |
| `py -m tools.language_audit.boxscore_parity 2025-06-14` | MLB play-by-play -> BLE -> box score |
| `py -m tools.language_audit.reader_diff` | Every sample play the new reader reads differently from legacy |
| `py -m tools.output_snapshot check` | GameChanger freeze check |

Harvested corpora are research data; keep them out of the repo.

## Known gaps

- No public corpus was available for iScore beyond the samples, or for
  smaller apps (ScoreBook, Dugout Edge, Rizzler, Baseball Stats
  Tracker). Their text needs real exports to verify.
- iScore `Strike 1.` pitch lines do not say looking/swinging, so they
  are not turned into swing decisions.
- MLB Gameday summary pages carry no pitch-by-pitch text, so MLB swing
  decisions need the pitch view.
