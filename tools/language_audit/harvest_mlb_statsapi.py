"""
Harvest MLB Stats API play descriptions with structured truth labels.

Usage:
    py -m tools.language_audit.harvest_mlb_statsapi <out.jsonl> [sportId] [YYYY-MM-DD ...]

sportId 1 = MLB, 11-14 = minor leagues. Output stays local (corpus is
research data, not committed).
"""
import json
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

OUT = Path(sys.argv[1])
SPORT = sys.argv[2] if len(sys.argv) > 2 else "1"
DATES = sys.argv[3:] or ["2025-04-05", "2025-05-10", "2025-06-14", "2025-07-19", "2025-08-23", "2025-09-20"]


def get(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)


def game_pks():
    pks = []
    for d in DATES:
        data = get(f"https://statsapi.mlb.com/api/v1/schedule?sportId={SPORT}&date={d}")
        for date in data.get("dates", []):
            for g in date["games"]:
                if g["status"]["abstractGameState"] == "Final":
                    pks.append(g["gamePk"])
    return pks


def plays(pk):
    try:
        data = get(f"https://statsapi.mlb.com/api/v1/game/{pk}/playByPlay")
    except Exception as e:
        return []
    rows = []
    for p in data.get("allPlays", []):
        res = p.get("result", {})
        hit = None
        traj = None
        loc = None
        for ev in p.get("playEvents", []):
            hd = ev.get("hitData")
            if hd:
                traj = hd.get("trajectory")
                loc = hd.get("location")
        rows.append({
            "kind": "pa",
            "game": pk,
            "description": res.get("description"),
            "batter": p.get("matchup", {}).get("batter", {}).get("fullName"),
            "event": res.get("event"),
            "eventType": res.get("eventType"),
            "trajectory": traj,
            "hit_location": loc,
            "pitches": [
                ev.get("details", {}).get("description")
                for ev in p.get("playEvents", []) if ev.get("isPitch")
            ],
        })
        for ev in p.get("playEvents", []):
            if not ev.get("isPitch") and ev.get("type") == "action":
                rows.append({
                    "kind": "action",
                    "game": pk,
                    "description": ev.get("details", {}).get("description"),
                    "event": ev.get("details", {}).get("event"),
                    "eventType": ev.get("details", {}).get("eventType"),
                })
    return rows


pks = game_pks()
print("games", len(pks))
with ThreadPoolExecutor(8) as ex:
    all_rows = [r for rows in ex.map(plays, pks) for r in rows]
OUT.write_text("\n".join(json.dumps(r) for r in all_rows), encoding="utf-8")
print("rows", len(all_rows))
