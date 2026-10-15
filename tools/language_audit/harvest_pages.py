"""
Harvest whole college box-score pages (SIDEARM or PrestoSports) the way a
coach would paste them, plus each page's official batting box.

For every box-score link on the given schedule pages, saves:
- ``text``: the page as plain text (block elements become new lines,
  table cells become tabs), like a select-all copy of the page
- ``box``: per-player H / BB / SO from the page's batting tables

Usage:
    py -m tools.language_audit.harvest_pages <out.jsonl> <sidearm|presto> <schedule-url> [...]

Polite by design: one request at a time, pauses between requests, and
backs off on rate limits. Output stays local (research data).
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
from html.parser import HTMLParser
from pathlib import Path


LINK_PATTERNS = {
    "sidearm": re.compile(r'href="([^"]*/sports/baseball/stats/\d{4}/[^"]+/boxscore/\d+)"'),
    "presto": re.compile(r'href="([^"]*/boxscores/[^"]+\.xml)"'),
}

_BLOCK_TAGS = {
    "p", "div", "section", "article", "header", "footer", "li", "ul", "ol",
    "table", "tbody", "thead", "tr", "h1", "h2", "h3", "h4", "h5", "h6",
    "br", "caption", "nav", "main", "aside", "dl", "dt", "dd",
}
_SKIP_TAGS = {"script", "style", "svg", "template"}


def _get(url: str) -> str:
    for attempt in range(5):
        time.sleep(3)
        request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return response.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as error:
            if error.code not in (429, 459, 503) or attempt == 4:
                raise
            time.sleep(45 * (attempt + 1))
    raise RuntimeError(url)


class _PageReader(HTMLParser):
    """Plain text like innerText, plus every table as rows of cell text."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip = 0
        self.tables: list[list[list[str]]] = []
        self.table_stack: list[list[list[str]]] = []
        self.cell: list[str] | None = None

    def handle_starttag(self, tag, attrs):
        if tag in _SKIP_TAGS:
            self.skip += 1
            return
        if tag in _BLOCK_TAGS:
            self.parts.append("\n")
        if tag == "table":
            self.table_stack.append([])
        elif tag == "tr" and self.table_stack:
            self.table_stack[-1].append([])
        elif tag in ("td", "th"):
            self.parts.append("\t")
            self.cell = []

    def handle_endtag(self, tag):
        if tag in _SKIP_TAGS:
            self.skip = max(0, self.skip - 1)
            return
        if tag in ("td", "th") and self.cell is not None and self.table_stack and self.table_stack[-1]:
            self.table_stack[-1][-1].append(" ".join(" ".join(self.cell).split()))
            self.cell = None
        elif tag == "table" and self.table_stack:
            self.tables.append(self.table_stack.pop())
        if tag in _BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data):
        if self.skip:
            return
        self.parts.append(data)
        if self.cell is not None:
            self.cell.append(data)

    def text(self) -> str:
        raw = "".join(self.parts)
        lines = [" ".join(line.split()) for line in raw.splitlines()]
        return "\n".join(line for line in lines if line)


def _batting_box(tables: list[list[list[str]]]) -> dict[str, dict[str, int]]:
    """Player -> H / BB / SO from tables whose header has AB, H, BB, SO."""
    box: dict[str, dict[str, int]] = {}

    for rows in tables:
        if not rows:
            continue
        header = [cell.strip().upper() for cell in rows[0]]
        # Batting tables only: SIDEARM pitching tables also carry AB/H/BB,
        # so any table with an IP column is skipped. SIDEARM's composite
        # batting table adds 2B / 3B / HR / SB / CS; every stat a table
        # has is collected and merged per player.
        if not {"AB", "H", "BB"} <= set(header) or "IP" in header:
            continue
        name_col = header.index("PLAYER") if "PLAYER" in header else 0
        index = {
            label: header.index(label)
            for label in _BOX_STATS
            if label in header
        }
        for row in rows[1:]:
            if len(row) <= max(index.values()):
                continue
            name = row[name_col].strip()
            if not name or name.lower().startswith(("totals", "team")):
                continue
            # Sidearm prints the position after the name ("Bryce Fowler cf").
            name = re.sub(r"\s+(?:[a-z]{1,2}|[0-9]b|dh|ph|pr)(?:/[a-z0-9]{1,2})*$", "", name)
            try:
                values = {key: int(row[col] or 0) for key, col in index.items()}
            except ValueError:
                continue
            box.setdefault(name, {}).update(values)

    return box


_BOX_STATS = ("H", "BB", "SO", "2B", "3B", "HR", "SB", "CS", "HBP")


def harvest_game(url: str, platform: str) -> dict | None:
    page_url = url + "?view=plays" if platform == "presto" else url
    try:
        page = _get(page_url)
    except Exception as error:
        print(f"skip {url}: {error}")
        return None

    reader = _PageReader()
    reader.feed(page)
    return {"url": url, "platform": platform, "text": reader.text(), "box": _batting_box(reader.tables)}


def main(argv: list[str]) -> int:
    out, platform, schedules = Path(argv[1]), argv[2], argv[3:]
    links: list[str] = []

    for schedule in schedules:
        try:
            page = _get(schedule)
        except Exception as error:
            print(f"skip schedule {schedule}: {error}")
            continue
        found = sorted({urllib.parse.urljoin(schedule, link) for link in LINK_PATTERNS[platform].findall(page)})
        print(f"{schedule}: {len(found)} box scores")
        links.extend(found)

    games = []
    with out.open("w", encoding="utf-8") as handle:
        for link in dict.fromkeys(links):
            game = harvest_game(link, platform)
            if game and game["box"]:
                games.append(game)
                handle.write(json.dumps(game) + "\n")
                handle.flush()

    print(f"games with a batting box: {len(games)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
