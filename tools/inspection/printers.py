from .constants import STAT_DISPLAY_ORDER


def section(title: str) -> None:
    print(f"\n{title}")
    print("-" * 40)


def subsection(title: str) -> None:
    print(f"\n{title}")
    print("=" * 40)