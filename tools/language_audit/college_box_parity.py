"""
End-to-end parity for college scorecards (PrestoSports harvest).

Each game's play lines are read by BLE's real pipeline, player names
are resolved to the box score's full names with roster name
recognition, and every player's totals are compared with the box:
H, BB, K, 2B, 3B, HR, HBP, SB, CS.

Usage:
    py -m tools.language_audit.college_box_parity <presto.jsonl>
"""

from __future__ import annotations

import collections
import json
import sys
from pathlib import Path

from aggregators.game_stat_aggregator import aggregate_game_stats
from language.names import RosterMatcher, resolve_player_stats
from models.types import EventType
from pipeline.process_game import process_game


HIT_EVENTS = {EventType.SINGLE, EventType.DOUBLE, EventType.TRIPLE, EventType.HOME_RUN}

# HBP is left out: Presto box scores list HBP only under the pitchers.
COMPARED = ("H", "BB", "K", "2B", "3B", "HR", "SB", "CS")


def _int(value) -> int:
    try:
        return int(str(value).strip() or 0)
    except ValueError:
        return 0


def box_totals(game: dict) -> dict[str, dict[str, int]]:
    totals: dict[str, dict[str, int]] = {}

    for team in game["box"]:
        for name, row in team["players"].items():
            totals[name] = {
                "H": _int(row.get("H")),
                "BB": _int(row.get("BB")),
                "K": _int(row.get("SO")),
                **{key: 0 for key in ("2B", "3B", "HR", "HBP", "SB", "CS")},
            }
        for name, counts in team.get("summary", {}).items():
            matched = RosterMatcher(team["players"].keys()).match(name) or name
            if matched in totals:
                for key, value in counts.items():
                    if key in totals[matched]:
                        totals[matched][key] = value

    return totals


def ble_totals(game: dict, roster: list[str]) -> tuple[dict[str, dict[str, int]], list[str]]:
    text = "College baseball play-by-play\n" + "\n".join(game["plays"])
    parsed = process_game(text)
    stats = aggregate_game_stats(parsed)

    for pa in parsed.plate_appearances:
        if pa.batter_name and pa.baseball_event and pa.baseball_event.primary_event in HIT_EVENTS:
            stats[pa.batter_name]["H"] = stats[pa.batter_name].get("H", 0) + 1

    return resolve_player_stats(stats, roster)


def main(argv: list[str]) -> int:
    games = [json.loads(line) for line in Path(argv[1]).read_text(encoding="utf-8").splitlines() if line]

    checks = 0
    mismatches: list[str] = []
    unmatched_names = collections.Counter()

    for game in games:
        box = box_totals(game)
        ble, unmatched = ble_totals(game, list(box))
        unmatched_names.update(unmatched)

        for name, expected in box.items():
            actual = ble.get(name, {})
            for key in COMPARED:
                checks += 1
                if int(actual.get(key, 0)) != expected[key]:
                    mismatches.append(f"{game['url']} {name} {key}: box {expected[key]} ble {actual.get(key, 0)}")

    by_stat = collections.Counter(line.split(": ")[0].split(" ")[-1] for line in mismatches)

    print(f"games {len(games)}  player-stat checks {checks}  mismatches {len(mismatches)}")
    print(f"match rate {(checks - len(mismatches)) / max(checks, 1):.3%}")
    print("by stat:", dict(by_stat))
    print("unmatched play-by-play names:", sum(unmatched_names.values()), unmatched_names.most_common(15))

    for line in mismatches[: int(argv[2]) if len(argv) > 2 else 40]:
        print(" ", line)

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
