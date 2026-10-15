# Master Plan: Read Every Scoring Platform Into Opponent IQ

Goal: any coach captures a game from any app with a meaningful client
base, and Opponent IQ turns it into the same stats, with the right
player names, as it does for GameChanger today.

## How a game gets in

```
coach's browser (logged in)
   -> IQ Capture extension reads the page text (plays + box score)
   -> Opponent IQ backend (app.opponentiq.com)
        GameChanger -> Opponent IQ Legacy parser (frozen, live)
        everything else -> BLE (pinned commit in requirements-backend.txt)
   -> name recognition against the box score / roster
   -> Opponent IQ stats, reports, exports
```

Two rules hold for every platform:

1. Text is read from what the coach can already see. Apps that need a
   login (PlayMaker, AthletesGoLive, iScore premium) are read through
   IQ Capture in the coach's own logged-in browser, never by BLE
   logging in.
2. Every platform gets the same proof before it ships: a language audit
   on real games, a box-score parity check, and phrase tests.

## Platform status

| Platform | Who uses it | Wording family | Public access | BLE status |
|---|---|---|---|---|
| GameChanger | HS, travel, youth (largest) | GameChanger present tense | Login | Live via Legacy; BLE frozen copy |
| MLB Gameday / StatsAPI | Pro, MiLB | Gameday present tense | Public | 99.8% read; 99.988% box parity (89 games) |
| ESPN | College + MLB | ESPN generated past tense | Public | 99.6% / 99.9% read |
| NCAA StatCrew family: Sidearm, PrestoSports, StatBroadcast, NCAA stats | D1 to JUCO, NAIA | StatCrew past tense + pitch codes | Public | 99.6% read; **99.77% box parity (103 Presto games)**; Sidearm D1 game read 83/83 |
| Presto scorecards scored GameChanger-style | Small colleges | GameChanger present tense | Public | Read (cleaner accepts present tense) |
| iScore | HS, travel | iScore ("hits a medium line drive for a single") | Viewer currently 502; premium for PBP | Samples read; needs live corpus |
| AthletesGoLive | Travel, summer collegiate, HS (MaxPreps partner) | Unknown until captured | Login (API returns 401) | Needs one IQ Capture sample |
| PlayMaker | AAU / tournaments | Unknown until captured | Free fan account | Needs one IQ Capture sample |
| ScoreBook, Dugout Edge, Rizzler, Baseball Stats Tracker | Small, growing | Unknown | Varies | Watch list |
| TrackMan / Yakkertech CSV | College, HS programs | Structured columns, not language | Coach exports | Mapper (no parsing needed) |

## Phases

### Phase A — done in this work
- Multi-platform reader (`language/`) for every non-GameChanger source.
- Freeze guard for GameChanger readings.
- Language audit, MLB box parity, college box parity, reader diff tools.
- Roster name recognition (`language/names.py`) used by the Opponent IQ
  adapter: initials, "Last, First", all caps, jersey prefixes, accents,
  abbreviated first names, Presto 12-character truncation; ambiguous
  names stay unmatched.
- GameChanger fixes in BLE: pitcher-fielded plays credit P; accented
  runner names.

### Phase B — iScore (next, largest unverified client base)
1. Retry the public iScore game list (`iscoretv.com/schedule_data.php`
   lists live and recent games with game hashes) once their viewer is
   back up; pull 50+ games of text.
2. Audit, fix phrasings, add phrase tests.
3. iScore `Strike 1.` pitch lines do not say called or swinging: decide
   how swing-decision reports treat them (count only, no swing split).

### Phase C — AthletesGoLive and PlayMaker (login apps)
1. Add both to IQ Capture's platform registry (host patterns
   `app.v2.athletesgolive.com`, `playmakerapp.io`).
   AthletesGoLive's game page loads play-by-play per inning as
   `batter_name`, `main_event` and detail lines; IQ Capture should read
   those lines in order.
2. One coach captures 3-5 games from each app.
3. Audit those games, add a cleaner + detection rule per app, phrase
   tests, then box parity against the app's own box score.

### Phase D — College coverage at scale
1. Harvest Sidearm D1 box scores (server-rendered, same StatCrew
   wording) the same way as Presto; run box parity.
2. StatBroadcast: same StatCrew XML wording; sample through IQ Capture
   (their site sits behind Cloudflare).
3. Per-team name resolution in parity (tell home from away by half
   inning) so two players named Smith on different teams never collide.

### Phase E — Ship to the live app (ON HOLD by owner decision, Oct 2026)

Nothing changes in the live app or the Opponent IQ Legacy parser until
the owner says so. Verified safe so far: the Opponent-IQ backend suite
gives identical results with this BLE as with the live pin.

1. Opponent-IQ backend pins BLE to one commit. Bump the pin only after
   the backend's own BLE tests pass against the new commit.
2. Shadow first: run the new BLE beside the pinned one on real captures
   (the backend already has `shadow_compare.py`) and review every
   difference.
3. GameChanger stays on the Opponent IQ Legacy parser. The two approved
   GameChanger fixes (pitcher credit, accented names) must be made in
   the Legacy parser itself to reach live GameChanger readings.

### Phase F — Keep it working
- Re-run the language audit and both parity checks monthly; platforms
  change their wording without notice.
- Every new phrasing found becomes a phrase test before it is fixed.
- Watch list apps move to Phase C when a coach asks for them.

## Open items that need a coach or the owner
- 3-5 captured games each from AthletesGoLive and PlayMaker.
- Confirm which smaller apps (ScoreBook, Dugout Edge, ...) clients use.
- Approve bumping the backend's BLE pin after shadow review.
