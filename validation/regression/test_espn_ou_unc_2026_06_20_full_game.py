from collections import Counter
from pathlib import Path

from detectors.source_detector import SourceType, detect_source
from pipeline.process_game import process_game


FIXTURE = Path(
    "samples/college/raw/"
    "espn_ou_vs_unc_2026_06_20_ou9_unc3_cws.txt"
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

OU_PLAYERS = {
    "J. Walk",
    "C. Johnson",
    "D. Lachance",
    "J. Willits",
    "T. Gambill",
    "B. Brock",
    "D. Harris",
    "D. Tockey",
    "K. Branch",
}

UNC_PLAYERS = {
    "J. Schaffner",
    "O. Hull",
    "G. Gallaher",
    "E. Paulsen",
    "C. Nicholson",
    "T. Howe",
    "C. Hynek",
    "M. Winslow",
    "R. Kellis V",
    "C. French",
}


def _event_name(pa) -> str:
    baseball_event = getattr(pa, "baseball_event", None)
    primary = getattr(baseball_event, "primary_event", None)

    if primary is None:
        return "NONE"

    return getattr(
        primary,
        "name",
        str(primary).split(".")[-1],
    )


def _player_totals(game) -> dict[str, Counter]:
    totals: dict[str, Counter] = {}

    for pa in game.plate_appearances:
        event = _event_name(pa)

        if event in RUNNER_ONLY_EVENTS:
            continue

        batter = pa.batter_name

        if not batter:
            continue

        stats = totals.setdefault(batter, Counter())
        stats["PA"] += 1

        if event == "SINGLE":
            stats["H"] += 1
            stats["1B"] += 1
            stats["AB"] += 1

        elif event == "DOUBLE":
            stats["H"] += 1
            stats["2B"] += 1
            stats["AB"] += 1

        elif event == "TRIPLE":
            stats["H"] += 1
            stats["3B"] += 1
            stats["AB"] += 1

        elif event == "HOME_RUN":
            stats["H"] += 1
            stats["HR"] += 1
            stats["AB"] += 1

        elif event == "WALK":
            stats["BB"] += 1

        elif event == "HIT_BY_PITCH":
            stats["HBP"] += 1

        elif event == "SAC_FLY":
            stats["SF"] += 1

        elif event == "SAC_BUNT":
            stats["SH"] += 1

        else:
            stats["AB"] += 1

        if event in {
            "STRIKEOUT_SWINGING",
            "STRIKEOUT_LOOKING",
        }:
            stats["K"] += 1

    return totals


def _team_totals(
    player_totals: dict[str, Counter],
    roster: set[str],
) -> Counter:
    totals = Counter()

    for player in roster:
        totals.update(player_totals.get(player, Counter()))

    return totals


def test_espn_ou_unc_fixture_is_detected_as_college():
    raw_text = FIXTURE.read_text(encoding="utf-8")

    assert detect_source(raw_text) == SourceType.COLLEGE


def test_espn_ou_unc_full_game_object_counts():
    raw_text = FIXTURE.read_text(encoding="utf-8")
    game = process_game(raw_text)

    batting_objects = [
        pa
        for pa in game.plate_appearances
        if _event_name(pa) not in RUNNER_ONLY_EVENTS
    ]

    runner_objects = [
        pa
        for pa in game.plate_appearances
        if _event_name(pa) in RUNNER_ONLY_EVENTS
    ]

    assert len(game.plate_appearances) == 88
    assert len(batting_objects) == 81
    assert len(runner_objects) == 7

    assert all(
        pa.batter_name is None
        for pa in runner_objects
    )


def test_espn_ou_unc_matches_verified_team_box_score():
    raw_text = FIXTURE.read_text(encoding="utf-8")
    game = process_game(raw_text)

    players = _player_totals(game)

    ou = _team_totals(players, OU_PLAYERS)
    unc = _team_totals(players, UNC_PLAYERS)

    assert {
        "AB": ou["AB"],
        "H": ou["H"],
        "HR": ou["HR"],
        "BB": ou["BB"],
        "HBP": ou["HBP"],
        "SF": ou["SF"],
        "SH": ou["SH"],
    } == {
        "AB": 37,
        "H": 14,
        "HR": 2,
        "BB": 2,
        "HBP": 0,
        "SF": 0,
        "SH": 2,
    }

    assert {
        "AB": unc["AB"],
        "H": unc["H"],
        "HR": unc["HR"],
        "BB": unc["BB"],
        "HBP": unc["HBP"],
        "SF": unc["SF"],
        "SH": unc["SH"],
    } == {
        "AB": 33,
        "H": 7,
        "HR": 0,
        "BB": 4,
        "HBP": 2,
        "SF": 1,
        "SH": 0,
    }


def test_espn_ou_unc_key_player_box_score_totals():
    raw_text = FIXTURE.read_text(encoding="utf-8")
    game = process_game(raw_text)

    players = _player_totals(game)

    assert players["J. Walk"]["AB"] == 5
    assert players["J. Walk"]["H"] == 2

    assert players["C. Johnson"]["AB"] == 4
    assert players["C. Johnson"]["H"] == 2
    assert players["C. Johnson"]["BB"] == 1

    assert players["D. Lachance"]["AB"] == 5
    assert players["D. Lachance"]["H"] == 3
    assert players["D. Lachance"]["HR"] == 2

    assert players["J. Willits"]["AB"] == 5
    assert players["J. Willits"]["H"] == 2

    assert players["K. Branch"]["AB"] == 3
    assert players["K. Branch"]["H"] == 1
    assert players["K. Branch"]["SH"] == 1

    assert players["D. Tockey"]["AB"] == 3
    assert players["D. Tockey"]["H"] == 1
    assert players["D. Tockey"]["SH"] == 1

    assert players["C. Hynek"]["AB"] == 3
    assert players["C. Hynek"]["H"] == 1
    assert players["C. Hynek"]["SF"] == 1


def test_espn_ou_unc_baserunning_totals_and_runner_identity():
    raw_text = FIXTURE.read_text(encoding="utf-8")
    game = process_game(raw_text)

    runner_events = [
        runner_event
        for pa in game.plate_appearances
        for runner_event in pa.runner_events
    ]

    stolen_bases = [
        event
        for event in runner_events
        if event.event_type == "SB"
    ]

    caught_stealing = [
        event
        for event in runner_events
        if event.event_type == "CS"
    ]

    assert {
        event.runner_name
        for event in stolen_bases
    } == {
        "J. Walk",
        "C. Johnson",
        "K. Branch",
    }

    assert len(stolen_bases) == 3
    assert len(caught_stealing) == 1

    assert caught_stealing[0].runner_name == "J. Willits"
    assert caught_stealing[0].base == "2B"
