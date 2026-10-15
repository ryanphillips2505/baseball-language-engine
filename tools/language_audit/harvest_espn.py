"""
Harvest ESPN play text with ESPN play type labels.

Usage:
    py -m tools.language_audit.harvest_espn <out.jsonl> <college-baseball|mlb> YYYYMMDD [...]

Output stays local (corpus is research data, not committed).
"""
import json
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

OUT = Path(sys.argv[1])
LEAGUE = sys.argv[2]  # college-baseball | mlb
DATES = sys.argv[3:]


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def events():
    ids = []
    for d in DATES:
        try:
            data = get(f"https://site.api.espn.com/apis/site/v2/sports/baseball/{LEAGUE}/scoreboard?dates={d}&limit=300")
        except Exception:
            continue
        for e in data.get("events", []):
            if e.get("status", {}).get("type", {}).get("completed"):
                ids.append(e["id"])
    return ids


def plays(eid):
    try:
        data = get(f"https://site.api.espn.com/apis/site/v2/sports/baseball/{LEAGUE}/summary?event={eid}")
    except Exception:
        return []
    rows = []
    for p in data.get("plays", []) or []:
        rows.append({
            "game": eid,
            "text": p.get("text"),
            "type": (p.get("type") or {}).get("text"),
            "type_id": (p.get("type") or {}).get("type"),
            "playType": (p.get("playType") or {}).get("text") if isinstance(p.get("playType"), dict) else None,
            "summaryType": p.get("summaryType"),
            "pitchType": (p.get("pitchType") or {}).get("text") if isinstance(p.get("pitchType"), dict) else None,
            "trajectory": p.get("trajectory"),
            "hitCoordinate": p.get("hitCoordinate"),
        })
    return rows


ids = events()
print("games", len(ids))
with ThreadPoolExecutor(8) as ex:
    all_rows = [r for rows in ex.map(plays, ids) for r in rows]
OUT.write_text("\n".join(json.dumps(r) for r in all_rows), encoding="utf-8")
print("rows", len(all_rows))
