from __future__ import annotations

from pathlib import Path


PA_START = "=== PA ==="
PA_END = "=== END ==="


def load_pa_blocks(file_path: str | Path) -> list[str]:
    """
    Load plate appearance blocks from a dataset text file.

    This does not parse baseball meaning.
    It only returns clean PA block strings.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"PA block file not found: {path}")

    text = path.read_text(encoding="utf-8")

    blocks: list[str] = []
    current: list[str] = []
    inside_block = False

    for line in text.splitlines():
        stripped = line.strip()

        if stripped == PA_START:
            inside_block = True
            current = []
            continue

        if stripped == PA_END:
            if inside_block and current:
                blocks.append("\n".join(current).strip())
            inside_block = False
            current = []
            continue

        if inside_block:
            current.append(line)

    return blocks
