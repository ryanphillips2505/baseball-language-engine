#!/usr/bin/env python3
"""Fetch and preserve MLB StatsAPI live-feed fixtures.

Usage:
  python tools/mlb/fetch_statsapi_fixture.py --game-pk 824988 \\
      --stem mlb_angels_athletics_2026_06_20_gamepk824988

Writes:
  samples/mlb/statsapi/raw/<stem>.live.json
  samples/mlb/statsapi/expected/<stem>.expected.json

The live.json body is preserved exactly as returned by StatsAPI.
Expected JSON is derived from that same response for validation.
"""

from __future__ import annotations

import argparse
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "samples" / "mlb" / "statsapi" / "raw"
EXPECTED_DIR = ROOT / "samples" / "mlb" / "statsapi" / "expected"
USER_AGENT = "Mozilla/5.0 (Baseball Language Engine fixture fetch)"


def fetch_live_feed(game_pk: int) -> bytes:
    endpoint = f"https://statsapi.mlb.com/api/v1.1/game/{game_pk}/feed/live"
    request = urllib.request.Request(
        endpoint,
        headers={"User-Agent": USER_AGENT},
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.read()


def build_expected(game_pk: int, endpoint: str, feed: dict) -> dict:
    box = feed["liveData"]["boxscore"]["teams"]
    plays = feed["liveData"]["plays"]["allPlays"]
    batting_keys = [
        "hits",
        "doubles",
        "triples",
        "homeRuns",
        "baseOnBalls",
        "strikeOuts",
        "hitByPitch",
        "atBats",
        "runs",
        "rbi",
        "stolenBases",
        "caughtStealing",
        "sacFlies",
        "sacBunts",
    ]

    def team_batting(side: str) -> dict:
        return {
            key: box[side]["teamStats"]["batting"].get(key)
            for key in batting_keys
        }

    return {
        "game_pk": game_pk,
        "official_date": feed["gameData"]["datetime"]["officialDate"],
        "away_team": feed["gameData"]["teams"]["away"]["name"],
        "home_team": feed["gameData"]["teams"]["home"]["name"],
        "endpoint": endpoint,
        "all_plays_count": len(plays),
        "all_play_descriptions": [
            play.get("result", {}).get("description")
            for play in plays
            if play.get("result", {}).get("description")
        ],
        "all_play_events": [
            {
                "at_bat_index": play.get("about", {}).get("atBatIndex"),
                "inning": play.get("about", {}).get("inning"),
                "half_inning": play.get("about", {}).get("halfInning"),
                "event": play.get("result", {}).get("event"),
                "event_type": play.get("result", {}).get("eventType"),
                "description": play.get("result", {}).get("description"),
                "batter": ((play.get("matchup") or {}).get("batter") or {}).get(
                    "fullName"
                ),
                "pitcher": ((play.get("matchup") or {}).get("pitcher") or {}).get(
                    "fullName"
                ),
                "rbi": play.get("result", {}).get("rbi"),
            }
            for play in plays
        ],
        "team_batting": {
            "away": team_batting("away"),
            "home": team_batting("home"),
        },
        "linescore": feed["liveData"]["linescore"]["teams"],
    }


def update_manifest(stem: str, game_pk: int, feed: dict, raw_bytes: int) -> None:
    manifest_path = RAW_DIR / "manifest.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    else:
        manifest = {
            "source": "statsapi.mlb.com",
            "fixtures": [],
        }

    manifest["retrieved_at_utc"] = datetime.now(timezone.utc).isoformat()
    entry = {
        "game_pk": game_pk,
        "stem": stem,
        "raw_path": f"samples/mlb/statsapi/raw/{stem}.live.json",
        "expected_path": f"samples/mlb/statsapi/expected/{stem}.expected.json",
        "official_date": feed["gameData"]["datetime"]["officialDate"],
        "away_team": feed["gameData"]["teams"]["away"]["name"],
        "home_team": feed["gameData"]["teams"]["home"]["name"],
        "bytes": raw_bytes,
        "all_plays_count": len(feed["liveData"]["plays"]["allPlays"]),
    }

    fixtures = [
        item
        for item in manifest.get("fixtures", [])
        if item.get("stem") != stem
    ]
    fixtures.append(entry)
    fixtures.sort(key=lambda item: item["stem"])
    manifest["fixtures"] = fixtures
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch and preserve an MLB StatsAPI live-feed fixture"
    )
    parser.add_argument("--game-pk", type=int, required=True)
    parser.add_argument(
        "--stem",
        required=True,
        help="Stable filename stem, e.g. mlb_angels_athletics_2026_06_20_gamepk824988",
    )
    args = parser.parse_args()

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    EXPECTED_DIR.mkdir(parents=True, exist_ok=True)

    endpoint = f"https://statsapi.mlb.com/api/v1.1/game/{args.game_pk}/feed/live"
    raw_bytes = fetch_live_feed(args.game_pk)
    feed = json.loads(raw_bytes)

    raw_path = RAW_DIR / f"{args.stem}.live.json"
    raw_path.write_bytes(raw_bytes)

    expected = build_expected(args.game_pk, endpoint, feed)
    expected_path = EXPECTED_DIR / f"{args.stem}.expected.json"
    expected_path.write_text(
        json.dumps(expected, indent=2) + "\n",
        encoding="utf-8",
    )

    update_manifest(args.stem, args.game_pk, feed, len(raw_bytes))

    print(f"Wrote {raw_path} ({len(raw_bytes)} bytes)")
    print(f"Wrote {expected_path}")
    print(
        f"{expected['away_team']} @ {expected['home_team']} "
        f"on {expected['official_date']}: {expected['all_plays_count']} plays"
    )


if __name__ == "__main__":
    main()
