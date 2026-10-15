"""
Harvest PrestoSports college scorecards: play-by-play plus box score.

For every box score linked from a team schedule page, saves the play
lines in order and each team's batting box (full player names, AB, H,
BB, SO and the 2B / 3B / HR / SB / CS / HBP / SF / SH summary lists).

Usage:
    py -m tools.language_audit.harvest_presto <out.jsonl> <schedule-url> [...]

Example schedule URL:
    https://crcpioneers.com/sports/bsb/2025-26/schedule

Output stays local (research data, not committed).
"""

from __future__ import annotations

import html
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


def _get(url: str) -> str:
    # Be polite: these are small school sites. Pause between requests
    # and back off when the host rate-limits (HTTP 429 / 459).
    for attempt in range(5):
        time.sleep(1.5)
        request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return response.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as error:
            if error.code not in (429, 459, 503) or attempt == 4:
                raise
            time.sleep(30 * (attempt + 1))
    raise RuntimeError(url)


def _text(fragment: str) -> str:
    fragment = re.sub(r"(?s)<[^>]+>", " ", fragment)
    return re.sub(r"\s+", " ", html.unescape(fragment)).strip()


def boxscore_links(schedule_url: str) -> list[str]:
    try:
        page = _get(schedule_url)
    except Exception as error:
        print(f"skip {schedule_url}: {error}")
        return []
    links =re.findall(r'href="([^"]*/boxscores/[^"]+\.xml)"', page)
    return sorted({urllib.parse.urljoin(schedule_url, link) for link in links})


def _plays(page: str) -> list[str]:
    # The plays tab opens with a scoring summary; the full play-by-play
    # starts at the first half-inning header after it.
    start = page.find("tab-panel plays")
    start = page.find("Top of", start if start != -1 else 0)
    panel = page[start:] if start != -1 else page
    plays = []
    for cell in re.findall(r'(?s)<td class="text">(.*?)</td>', panel):
        line = _text(cell)
        line = re.sub(r"\s*\(\d out[s]?\)\s*$", "", line)
        if line:
            plays.append(line)
    return plays


_SUMMARY_KEYS = ("2B", "3B", "HR", "SB", "CS", "HBP", "SF", "SH")


def _summary_counts(block: str) -> dict[str, dict[str, int]]:
    counts: dict[str, dict[str, int]] = {}
    for key in _SUMMARY_KEYS:
        match = re.search(rf"(?s)<strong>{re.escape(key)}:</strong>\s*<span>(.*?)</span>", block)
        if not match:
            continue
        for item in _text(match.group(1)).split(","):
            item = item.strip()
            if not item:
                continue
            number = re.search(r"\((\d+)\)\s*$", item)
            name = re.sub(r"\s*\(\d+\)\s*$", "", item).strip()
            counts.setdefault(name, {})[key] = int(number.group(1)) if number else 1
    return counts


def _box(page: str) -> list[dict]:
    teams = []
    tables = list(re.finditer(r'(?s)<table class="table\s+table-striped striped">.*?</table>', page))
    hitters = [m for m in tables if "Hitters" in m.group(0)]

    for index, match in enumerate(hitters):
        table = match.group(0)
        headers = [_text(h) for h in re.findall(r'(?s)<th scope="col"[^>]*>(.*?)</th>', table)]
        players = {}
        for row in re.findall(r"(?s)<tr>(.*?)</tr>", table):
            name = re.search(r'(?s)class="player-name[^"]*">(.*?)</a>', row)
            if not name:
                continue
            cells = [_text(c) for c in re.findall(r"(?s)<td>(.*?)</td>", row)]
            players[_text(name.group(1))] = dict(zip(headers[1:], cells))

        # Summary lists ("2B: James Wilson , Ricky Requena") sit between
        # this batting table and the next one.
        segment_end = hitters[index + 1].start() if index + 1 < len(hitters) else len(page)
        segment = page[match.end():segment_end]
        teams.append({"players": players, "summary": _summary_counts(segment)})

    return teams


def harvest_game(url: str) -> dict | None:
    try:
        page = _get(url + "?view=plays")
    except Exception:
        return None
    return {"url": url, "plays": _plays(page), "box": _box(page)}


def main(argv: list[str]) -> int:
    out = Path(argv[1])
    links = [link for schedule in argv[2:] for link in boxscore_links(schedule)]

    with ThreadPoolExecutor(2) as pool:
        games = [game for game in pool.map(harvest_game, links) if game and game["plays"]]

    out.write_text("\n".join(json.dumps(game) for game in games), encoding="utf-8")
    print(f"games {len(games)} plays {sum(len(g['plays']) for g in games)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
