"""
PlayMaker parity: each game page's play-by-play -> BLE -> per-player H, BB,
K compared with the batting boxes printed on the same page.

Usage:
    py -m tools.language_audit.playmaker_parity <games.json>

games.json: {"<game url>": "<page text as a coach copies it>", ...}
"""

from __future__ import annotations

import collections
import json
import re
import sys
from pathlib import Path

from aggregators.game_stat_aggregator import aggregate_game_stats
from detectors.source_detector import detect_source
from language.names import resolve_player_stats
from pipeline.process_game import process_game

_BOX_HEADER = ["BATTING", "AB", "R", "H", "RBI", "BB", "K", "LOB"]
_INT_RE = re.compile(r"^\d+$")


def batting_boxes(text: str) -> list[dict[str, dict[str, int]]]:
    """Every BATTING table on the page: player -> {AB, R, H, RBI, BB, K}."""
    lines = [" ".join(line.split()) for line in str(text or "").splitlines()]
    lines = [line for line in lines if line]
    boxes = []
    index = 0
    while index < len(lines):
        if lines[index : index + len(_BOX_HEADER)] != _BOX_HEADER:
            index += 1
            continue
        index += len(_BOX_HEADER)
        box: dict[str, dict[str, int]] = {}
        while index < len(lines) and lines[index] != "Totals":
            name = lines[index]
            index += 1
            # Optional position ("SS", "1B", "DH"); some rows have none.
            if index < len(lines) and not _INT_RE.match(lines[index]):
                index += 1
            numbers = lines[index : index + 7]
            if len(numbers) < 7 or not all(_INT_RE.match(n) for n in numbers):
                break
            index += 7
            ab, r, h, rbi, bb, k, _lob = (int(n) for n in numbers)
            box[name] = {"AB": ab, "R": r, "H": h, "RBI": rbi, "BB": bb, "K": k}
        totals = lines[index + 1 : index + 8] if index < len(lines) and lines[index] == "Totals" else []
        boxes.append({"rows": box, "totals": [int(n) for n in totals] if all(_INT_RE.match(n) for n in totals) else []})
    return boxes


def usable_box(box: dict) -> dict[str, dict[str, int]]:
    """
    Rows that can judge BLE. PlayMaker sometimes prints rows with no real
    name ("E.", ". Mikey Hannaberry") or leaves hitters out entirely; a box
    whose rows do not add up to its Totals line is skipped.
    """
    rows = box["rows"]
    totals = box["totals"]
    if len(totals) < 6:
        return {}
    for position, key in ((0, "AB"), (2, "H"), (4, "BB"), (5, "K")):
        if sum(row[key] for row in rows.values()) != totals[position]:
            return {}
    return {
        name: stats
        for name, stats in rows.items()
        if _NAMED_ROW_RE.match(name)
    }


_NAMED_ROW_RE = re.compile(r"^[A-ZÀ-Þ][\w'\-]*\.?\s+[A-ZÀ-Þ][\w'\-]")


def score_game(text: str) -> tuple[str, int, int, list[str]]:
    source = detect_source(text).value
    stats = aggregate_game_stats(process_game(text))
    checks = errors = 0
    misses: list[str] = []
    for raw_box in batting_boxes(text):
        box = usable_box(raw_box)
        if not box:
            continue
        resolved, _unmatched = resolve_player_stats(stats, list(raw_box["rows"]))
        for name, expected in box.items():
            got = resolved.get(name, {})
            for key in ("H", "BB", "K"):
                checks += 1
                if int(got.get(key, 0) or 0) != expected[key]:
                    errors += 1
                    misses.append(f"{name} {key}: box {expected[key]} ble {got.get(key, 0)}")
    return source, checks, errors, misses


def main(argv: list[str]) -> int:
    games = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    sources = collections.Counter()
    total_checks = total_errors = 0
    worst = []
    for url, text in games.items():
        if "BATTING" not in text:
            continue
        source, checks, errors, misses = score_game(text)
        sources[source] += 1
        total_checks += checks
        total_errors += errors
        if errors:
            worst.append((errors, url, misses[:5]))
    print("detected source:", dict(sources))
    print(
        f"games {sum(sources.values())} | player-stat checks {total_checks} | "
        f"errors {total_errors} | match {(total_checks - total_errors) / max(total_checks, 1):.2%}"
    )
    for errors, url, misses in sorted(worst, reverse=True)[:15]:
        print(f"  {errors:3} {url}")
        for miss in misses:
            print(f"        {miss}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
