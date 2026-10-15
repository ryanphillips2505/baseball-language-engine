"""
Whole-page parity: a SIDEARM / Presto box-score page pasted as text ->
BLE -> every per-player stat in the page's batting box compared with the same page's batting box.

Usage:
    py -m tools.language_audit.page_box_parity <pages.jsonl> [<pages.jsonl> ...]
"""

from __future__ import annotations

import collections
import json
import sys
from pathlib import Path

from aggregators.game_stat_aggregator import aggregate_game_stats
from detectors.source_detector import detect_source_with_language_fallbacks
from language.names import resolve_player_stats
from pipeline.process_game import process_game


per_stat: dict[str, list[int]] = collections.defaultdict(lambda: [0, 0])


def score_page(page: dict) -> tuple[str, int, int, list[str]]:
    text = page["text"]
    box = page["box"]
    source = detect_source_with_language_fallbacks(text).value

    stats = aggregate_game_stats(process_game(text))
    resolved, _unmatched = resolve_player_stats(stats, list(box))

    checks = errors = 0
    misses: list[str] = []
    for name, expected in box.items():
        got = resolved.get(name, {})
        for box_key, value in expected.items():
            key = "K" if box_key == "SO" else box_key
            checks += 1
            per_stat[key][0] += 1
            if int(got.get(key, 0) or 0) != value:
                errors += 1
                per_stat[key][1] += 1
                misses.append(f"{name} {key}: box {value} ble {got.get(key, 0)}")
    return source, checks, errors, misses


def main(argv: list[str]) -> int:
    pages = [
        json.loads(line)
        for path in argv[1:]
        for line in Path(path).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    by_platform = collections.defaultdict(lambda: [0, 0, 0])
    sources = collections.Counter()
    worst: list[tuple[int, str, list[str]]] = []

    for page in pages:
        source, checks, errors, misses = score_page(page)
        sources[(page["platform"], source)] += 1
        totals = by_platform[page["platform"]]
        totals[0] += 1
        totals[1] += checks
        totals[2] += errors
        if errors:
            worst.append((errors, page["url"], misses[:4]))

    print("detected source per platform:", dict(sources))
    all_checks = sum(v[1] for v in by_platform.values())
    all_errors = sum(v[2] for v in by_platform.values())
    for platform, (games, checks, errors) in by_platform.items():
        print(f"{platform:8} games {games:4} | player-stat checks {checks:6} | errors {errors:4} | match {(checks - errors) / max(checks, 1):.2%}")
    print(f"ALL      games {sum(v[0] for v in by_platform.values()):4} | checks {all_checks} | errors {all_errors} | match {(all_checks - all_errors) / max(all_checks, 1):.2%}")

    print("per stat:", ", ".join(
        f"{key} {(c - e) / max(c, 1):.2%} ({e}/{c})" for key, (c, e) in sorted(per_stat.items())
    ))
    for errors, url, misses in sorted(worst, reverse=True)[:12]:
        print(f"  {errors:3} {url}")
        for miss in misses:
            print(f"        {miss}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
