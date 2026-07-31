from assemblers.plate_appearance_builder import build_plate_appearance
from models.types import EventType


def test_single_with_fielding_error_keeps_hit_and_error_secondary():
    text = (
        "Donovan Walton singles on a ground ball to right fielder Wilyer Abreu. "
        "Lawrence Butler scores. Jeff McNeil to 3rd. "
        "Fielding error by right fielder Wilyer Abreu."
    )
    pa = build_plate_appearance(text)
    assert pa.batter_name == "Donovan Walton"
    assert pa.baseball_event is not None
    assert pa.baseball_event.primary_event == EventType.SINGLE
    assert EventType.ERROR in pa.baseball_event.secondary_events


def test_double_with_throwing_error_advance_attaches_error_secondary():
    text = (
        "Ceddanne Rafaela doubles (27) on a ground ball to left fielder "
        "Tyler Soderstrom. Andruw Monasterio scores. Anthony Seigler scores. "
        "Ceddanne Rafaela to 3rd. Ceddanne Rafaela advances to 3rd, on a "
        "throwing error by shortstop Donovan Walton."
    )
    pa = build_plate_appearance(text)
    assert pa.batter_name == "Ceddanne Rafaela"
    assert pa.baseball_event is not None
    assert pa.baseball_event.primary_event == EventType.DOUBLE
    assert EventType.ERROR in pa.baseball_event.secondary_events


def test_fielders_choice_with_fielding_error_attaches_error_secondary():
    text = (
        "Joc Pederson reaches on a fielder's choice, fielded by shortstop "
        "Taylor Walls. Ezequiel Duran scores. Brandon Nimmo to 2nd. "
        "Fielding error by shortstop Taylor Walls."
    )
    pa = build_plate_appearance(text)
    assert pa.batter_name == "Joc Pederson"
    assert pa.baseball_event is not None
    assert pa.baseball_event.primary_event == EventType.FIELDERS_CHOICE
    assert EventType.ERROR in pa.baseball_event.secondary_events


def test_reach_on_error_stays_primary_error_without_duplicate_secondary():
    text = (
        "Nick Kurtz reaches on a fielding error by shortstop "
        "Andruw Monasterio. Carlos Cortes to 3rd."
    )
    pa = build_plate_appearance(text)
    assert pa.baseball_event is not None
    assert pa.baseball_event.primary_event == EventType.ERROR
    assert pa.baseball_event.secondary_events == []
