"""
End-to-end parity: MLB play-by-play -> BLE -> stats vs official box score.

For each game, the play descriptions from the MLB Stats API are
written out as one game text in order (runner actions before the plate
appearance they happened in) and read by BLE's real pipeline
(process_game -> aggregate_game_stats). Every player's totals are then
compared with the official box score.

Compared stats: K, BB, HBP, 2B, 3B, HR, SB, CS and BIP, where
    BIP = AB - K + SF + SH
(home runs and reached-on-error count as balls in play; catcher's
interference does not).

Usage:
    py -m tools.language_audit.boxscore_parity YYYY-MM-DD [YYYY-MM-DD ...]
"""

from __future__ import annotations

import collections
import json
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor

from aggregators.game_stat_aggregator import aggregate_game_stats
from pipeline.process_game import process_game


RUNNER_ACTIONS = {
    "stolen_base_2b", "stolen_base_3b", "stolen_base_home",
    "caught_stealing_2b", "caught_stealing_3b", "caught_stealing_home",
    "pickoff_1b", "pickoff_2b", "pickoff_3b",
    "pickoff_caught_stealing_2b", "pickoff_caught_stealing_3b", "pickoff_caught_stealing_home",
    "wild_pitch", "passed_ball", "balk", "defensive_indiff",
}

BOX_KEYS = {
    "K": "strikeOuts",
    "BB": "baseOnBalls",
    "HBP": "hitByPitch",
    "2B": "doubles",
    "3B": "triples",
    "HR": "homeRuns",
    "SB": "stolenBases",
    "CS": "caughtStealing",
}


def _get(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=60) as response:
        return json.load(response)


def game_pks(date: str) -> list[int]:
    data = _get(f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={date}")
    return [
        game["gamePk"]
        for day in data.get("dates", [])
        for game in day["games"]
        if game["status"]["abstractGameState"] == "Final"
    ]


def game_text(play_by_play: dict) -> str:
    lines = ["Major League Baseball"]

    for play in play_by_play.get("allPlays", []):
        for event in play.get("playEvents", []):
            details = event.get("details", {})
            if event.get("type") == "action" and details.get("eventType") in RUNNER_ACTIONS:
                if details.get("description"):
                    lines.append(details["description"])

        description = play.get("result", {}).get("description")
        if description:
            lines.append(description)

    return "\n".join(lines)


def box_totals(boxscore: dict) -> dict[str, dict[str, int]]:
    totals: dict[str, dict[str, int]] = {}

    for side in ("home", "away"):
        for player in boxscore["teams"][side]["players"].values():
            batting = player.get("stats", {}).get("batting") or {}
            if not batting:
                continue

            name = player["person"]["fullName"]
            row = {key: int(batting.get(source, 0)) for key, source in BOX_KEYS.items()}
            row["BIP"] = (
                int(batting.get("atBats", 0))
                - int(batting.get("strikeOuts", 0))
                + int(batting.get("sacFlies", 0))
                + int(batting.get("sacBunts", 0))
            )

            if any(row.values()) or batting.get("plateAppearances"):
                totals[name] = row

    return totals


def compare_game(game_pk: int) -> tuple[int, list[str]]:
    play_by_play = _get(f"https://statsapi.mlb.com/api/v1/game/{game_pk}/playByPlay")
    boxscore = _get(f"https://statsapi.mlb.com/api/v1/game/{game_pk}/boxscore")

    ble = aggregate_game_stats(process_game(game_text(play_by_play)))
    box = box_totals(boxscore)

    mismatches: list[str] = []
    compared = 0

    for name, expected in box.items():
        actual = ble.get(name, {})
        for key, value in expected.items():
            compared += 1
            got = int(actual.get(key, 0))
            if got != value:
                mismatches.append(f"{game_pk} {name} {key}: box {value} ble {got}")

    for name in ble:
        if name not in box and any(ble[name].get(key, 0) for key in ("K", "BB", "BIP", "SB")):
            mismatches.append(f"{game_pk} unknown player in BLE: {name!r}")

    return compared, mismatches


def main(argv: list[str]) -> int:
    dates = argv[1:] or ["2025-06-14"]
    pks = [pk for date in dates for pk in game_pks(date)]

    with ThreadPoolExecutor(8) as pool:
        results = list(pool.map(compare_game, pks))

    compared = sum(count for count, _ in results)
    mismatches = [line for _, lines in results for line in lines]

    by_stat = collections.Counter(
        line.split(": ")[0].split(" ")[-1] for line in mismatches if ": box" in line
    )

    print(f"games {len(pks)}  player-stat checks {compared}  mismatches {len(mismatches)}")
    print(f"match rate {(compared - len(mismatches)) / max(compared, 1):.3%}")
    print("by stat:", dict(by_stat))

    for line in mismatches[:60]:
        print(" ", line)

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
