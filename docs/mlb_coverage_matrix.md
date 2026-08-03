# MLB Coverage Matrix (Corpus-Scoped)

Claims below are **N-of-M on the checked fixtures only**. Do not generalize to “MLB is 100% accurate.”

Integration tip for Opponent IQ: pin BLE after merging the completion PR into `report-translators-phase`, then use `process_raw_text_to_opponent_iq_game(raw_text)`.

## Corpora

| Corpus | Fixtures | Notes |
|--------|----------|-------|
| Gameday validation (reconciled) | `rangers_rays_2026_07_30`, `marlins_mets_2026_07_30`, `redsox_athletics_2026_07_30`, `redsox_dodgers_2026_08_02`, `tigers_athletics_2026_08_02` | Full pastes / IQ Capture; boxscore sidecars |
| Gameday validation (sidecar only) | `red_sox_angels_2026_07_04` | Does **not** claim boxscore parity vs `824012` |
| StatsAPI live | gamePks `824988`, `823126`, `824012` | Nested actions + pitch events |

## Boxscore reconcile (Gameday → StatsAPI team batting)

On the three reconciled 2026-07-30 Gameday fixtures:

| Key | Claim |
|-----|-------|
| K, BB(+IBB), IBB, H, HR, 2B, 3B, HBP, sac bunt, sac fly, SB, CS | **60/60** keys match (`test_mlb_gameday_boxscore_reconcile.py`) |

## StatsAPI pitch / swing layer

| Claim | Scope |
|-------|-------|
| Pitch type / velocity / result on `game.pitch_events` | StatsAPI fixtures |
| `pa.pitches` as `PitchDecision` swing reports | Angels `824988`: **321/322** swing outcomes (1 HBP skipped) |

## Event / language coverage

| Concept | Status on corpus | Notes |
|---------|------------------|-------|
| Singles / doubles / triples / HR | Covered; H reconciles 3/3 | Aggregator counts `1B` for singles |
| Walk / intentional walk | Covered | IBB is distinct `intentional_walk`, still rolls into BB totals |
| HBP / K (looking+swinging) | Covered | |
| Sac bunt / sac fly | Covered | Sac-bunt ROE preserved |
| Ground-rule double | Covered | Remains `double` |
| Challenge / umpire review / ABS overturn notes | Quarantined | Admin / non-PA |
| Substitution / pitching change admin | Quarantined | `metadata.administrative=True` |
| Stolen base / caught stealing / pickoff / WP | Covered where present | Nested StatsAPI `playEvents` on timeline |
| Secondary error on hit / FC | Covered | Error stays secondary |
| Force out language | Maps to `fielders_choice` | Intentional: batter-reach force plays are FC for Opp IQ |
| Pitch type / velocity on Gameday text | Not invented | Gameday pastes have no pitch telemetry |
| ITPHR / triple play / CI / obstruction / automatic ball-strike | Absent from corpus | No claim |

## Opponent IQ adapter notes

Legacy key overload (unchanged intent, now includes singles):

- `1B` = singles + balls to first
- `2B` = doubles + balls to second
- `3B` = triples + balls to third

GameChanger remains on its existing path; do not globally switch all sources to BLE until Opponent IQ pins a verified commit and routes MLB only.
