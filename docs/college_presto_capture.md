# College / Presto Capture → BLE Accuracy

Workflow: paste full game play-by-play → land as fixture → measure → fix parser gaps until corpus eventization ≥ **99%**.

Claims stay **corpus-scoped** (N-of-M on checked fixtures). Do not generalize to “all college/Presto is 99%.”

## Paste format (what to send)

For each game, paste as much as possible in one message:

1. **Source label** — Presto / StatView / school athletics site / ESPN / other
2. **Matchup + date** — e.g. `Oklahoma vs Texas 2026-03-15`
3. **Full play-by-play** — every inning, including runner events if shown
4. **Box score totals** (optional but valuable) — team K/BB/H/HR/2B/3B/HBP/SF/SH/SB/CS

Do not clean or rewrite lines. Raw paste is better.

## Fixture layout

```
samples/college/presto/raw/<stem>.txt
samples/college/presto/expected/<stem>.boxscore.json   # optional
samples/college/presto/manifest.json
```

Stem convention: `away_home_YYYY_MM_DD` (lowercase, underscores).

## 99% accuracy contract

Primary metric (**eventization rate**):

```
eventized_play_lines / cleaned_play_lines >= 0.99
```

- Cleaned play lines = college/Presto cleaner output (action lines only)
- Eventized = `detect_event_types` → non-null `BaseballEvent`
- Target applies to the **whole Presto corpus** and to each game individually once ≥ 1 game exists

Secondary metric (when boxscore sidecar present):

- Team batting keys reconcile: K, BB, H, HR, 2B, 3B, HBP, SF, SH, SB, CS

## Commands

```bash
# Score current Presto corpus
python3 tools/college/score_presto_corpus.py

# Gate
python3 -m pytest tests/test_presto_corpus_accuracy.py -q
```

## Agent loop per paste batch

1. Save raw fixture(s) under `samples/college/presto/raw/`
2. Register in `manifest.json`
3. Score corpus; list undetected lines
4. Fix cleaner/detector/assembler only as needed
5. Re-score; keep GC / MLB / iScore / ESPN regressions green
6. Commit + push; update PR
