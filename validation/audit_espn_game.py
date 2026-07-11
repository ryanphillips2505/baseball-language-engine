from collections import Counter
from pathlib import Path

from pipeline.process_game import process_game


GAME_PATH = Path(
    "samples/college/raw/espn_ou_vs_unc_2026_06_20_ou9_unc3_cws.txt"
)

RUNNER_ONLY_EVENTS = {
    "STOLEN_BASE",
    "CAUGHT_STEALING",
    "PICKOFF",
    "PICKED_OFF",
    "WILD_PITCH",
    "WILD_PITCH_ADVANCE",
    "PASSED_BALL",
    "PASSED_BALL_ADVANCE",
    "RUNNER_ADVANCE",
    "RUNNER_OUT",
}


def event_name(pa):
    event = getattr(pa, "baseball_event", None)
    primary = getattr(event, "primary_event", None)

    if primary is None:
        return "NONE"

    return getattr(
        primary,
        "name",
        str(primary).split(".")[-1],
    )


def main():
    raw_text = GAME_PATH.read_text(encoding="utf-8")
    game = process_game(raw_text)

    all_event_counts = Counter()
    batting_event_counts = Counter()
    runner_event_counts = Counter()
    player_totals = {}

    batting_objects = []
    runner_objects = []

    for pa in game.plate_appearances:
        name = event_name(pa)
        all_event_counts[name] += 1

        if name in RUNNER_ONLY_EVENTS:
            runner_objects.append(pa)
            runner_event_counts[name] += 1
            continue

        batting_objects.append(pa)
        batting_event_counts[name] += 1

        batter = getattr(pa, "batter_name", None)

        if not batter:
            continue

        stats = player_totals.setdefault(
            batter,
            Counter(),
        )

        stats["PA"] += 1

        if name == "SINGLE":
            stats["H"] += 1
            stats["1B"] += 1

        elif name == "DOUBLE":
            stats["H"] += 1
            stats["2B"] += 1

        elif name == "TRIPLE":
            stats["H"] += 1
            stats["3B"] += 1

        elif name == "HOME_RUN":
            stats["H"] += 1
            stats["HR"] += 1

        elif name == "WALK":
            stats["BB"] += 1

        elif name == "HIT_BY_PITCH":
            stats["HBP"] += 1

        elif name in {
            "STRIKEOUT_SWINGING",
            "STRIKEOUT_LOOKING",
        }:
            stats["K"] += 1

        elif name == "SAC_FLY":
            stats["SF"] += 1

        elif name == "SAC_BUNT":
            stats["SH"] += 1

    print("\n===== GAME SUMMARY =====")
    print(f"Total parsed objects:       {len(game.plate_appearances)}")
    print(f"Batting/PA objects:         {len(batting_objects)}")
    print(f"Runner-only objects:        {len(runner_objects)}")
    print(
        "Objects reconcile:         "
        f"{len(batting_objects) + len(runner_objects) == len(game.plate_appearances)}"
    )

    print("\n===== ALL EVENT COUNTS =====")

    for name, count in sorted(all_event_counts.items()):
        print(f"{name:28} {count}")

    print("\n===== BATTING EVENT COUNTS =====")

    for name, count in sorted(batting_event_counts.items()):
        print(f"{name:28} {count}")

    print("\n===== RUNNER EVENT COUNTS =====")

    for name, count in sorted(runner_event_counts.items()):
        print(f"{name:28} {count}")

    print("\n===== PLAYER BATTING TOTALS =====")

    for player, stats in sorted(player_totals.items()):
        print(
            f"{player:20}"
            f" PA={stats['PA']:2}"
            f" H={stats['H']:2}"
            f" 1B={stats['1B']:2}"
            f" 2B={stats['2B']:2}"
            f" 3B={stats['3B']:2}"
            f" HR={stats['HR']:2}"
            f" BB={stats['BB']:2}"
            f" HBP={stats['HBP']:2}"
            f" K={stats['K']:2}"
            f" SF={stats['SF']:2}"
            f" SH={stats['SH']:2}"
        )

    print("\n===== RUNNER-ONLY OBJECTS =====")

    for pa in runner_objects:
        name = event_name(pa)
        raw_text = getattr(pa, "raw_text", None)

        if raw_text is None:
            raw_text = getattr(pa, "source_text", None)

        runner_events = getattr(pa, "runner_events", []) or []

        runner_details = [
            (
                getattr(event, "event_type", None),
                getattr(event, "base", None),
                getattr(event, "runner_name", None),
            )
            for event in runner_events
        ]

        print(
            f"{name:24} | "
            f"batter_field={getattr(pa, 'batter_name', None)!r} | "
            f"runner_events={runner_details!r} | "
            f"raw={raw_text!r}"
        )

    assert len(batting_objects) == 81
    assert len(runner_objects) == 7
    assert "J. Willits picked off and" not in player_totals

    print("\nPASS: Runner-only events are excluded from batting totals.")
    print("PASS: Oklahoma-UNC produces 81 batting objects and 7 runner-only objects.")


if __name__ == "__main__":
    main()
