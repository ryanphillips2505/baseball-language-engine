from pathlib import Path


def load_game_file(path: str | Path) -> list[str]:
    """
    Load a raw play-by-play file.

    Returns one play per list element.
    Blank lines separate plays.
    """

    text = Path(path).read_text(encoding="utf-8")

    plays = []

    current = []

    for line in text.splitlines():
        line = line.rstrip()

        if not line:
            if current:
                plays.append("\n".join(current))
                current = []
            continue

        current.append(line)

    if current:
        plays.append("\n".join(current))

    return plays