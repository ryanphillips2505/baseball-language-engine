from __future__ import annotations

from pathlib import Path

from extractors.mlb_boxscore_name_mapper import (
    map_box_tokens_to_full_names,
    parse_box_player_token,
)
from extractors.mlb_iq_capture_names import (
    build_box_to_pbp_name_map,
    extract_box_player_tokens,
)

FIXTURE = Path("samples/mlb/validation/redsox_dodgers_2026_08_02.txt")


def test_parse_box_tokens_common_shapes():
    sogard = parse_box_player_token("Sogard2B")
    assert sogard is not None
    assert sogard.last_name == "Sogard"
    assert sogard.initials is None
    assert sogard.position == "2B"

    dual = parse_box_player_token("CortesDH-P")
    assert dual is not None
    assert dual.last_name == "Cortes"
    assert dual.position == "DH-P"

    abreu = parse_box_player_token("Abreu, WRF")
    assert abreu is not None
    assert abreu.last_name == "Abreu"
    assert abreu.initials == "W"
    assert abreu.position == "RF"

    duran = parse_box_player_token("Duran, JaLF")
    assert duran is not None
    assert duran.last_name == "Duran"
    assert duran.initials == "Ja"
    assert duran.position == "LF"

    call = parse_box_player_token("a-CallPH-RF")
    assert call is not None
    assert call.last_name == "Call"
    assert call.position == "PH-RF"
    assert call.pinch_marker == "a"

    enrique = parse_box_player_token("b-Hernández, EPH-1B")
    assert enrique is not None
    assert enrique.last_name == "Hernández"
    assert enrique.initials == "E"
    assert enrique.position == "PH-1B"


def test_disambiguates_hernandez_brothers_by_initial():
    full = ["Teoscar Hernández", "Enrique Hernández"]
    mapping = map_box_tokens_to_full_names(
        ["Hernández, TLF", "b-Hernández, EPH-1B"],
        full,
    )
    assert mapping["Hernández, TLF"] == "Teoscar Hernández"
    assert mapping["b-Hernández, EPH-1B"] == "Enrique Hernández"


def test_iq_capture_box_to_pbp_map_redsox_dodgers():
    raw = FIXTURE.read_text(encoding="utf-8")
    tokens = extract_box_player_tokens(raw)
    assert "Sogard2B" in tokens
    assert "Abreu, WRF" in tokens
    assert "b-Hernández, EPH-1B" in tokens
    assert "WongC" in tokens

    mapping = build_box_to_pbp_name_map(raw)

    expected = {
        "Sogard2B": "Nick Sogard",
        "RafaelaCF": "Ceddanne Rafaela",
        "Abreu, WRF": "Wilyer Abreu",
        "Contreras, Wn1B": "Willson Contreras",
        "YoshidaDH": "Masataka Yoshida",
        "Durbin3B": "Caleb Durbin",
        "MonasterioSS": "Andruw Monasterio",
        "Duran, JaLF": "Jarren Duran",
        "NarváezC": "Carlos Narváez",
        "a-SeiglerPH": "Anthony Seigler",
        "WongC": "Connor Wong",
        "OhtaniDH": "Shohei Ohtani",
        "Pages, ACF": "Andy Pages",
        "Edman2B": "Tommy Edman",
        "Freeman, F1B": "Freddie Freeman",
        "a-CallPH-RF": "Alex Call",
        "BettsSS": "Mookie Betts",
        "TuckerRF": "Kyle Tucker",
        "b-Hernández, EPH-1B": "Enrique Hernández",
        "Hernández, TLF": "Teoscar Hernández",
        "Muncy3B": "Max Muncy",
        "AlfonzoC": "Eliezer Alfonzo",
    }

    for token, full in expected.items():
        assert mapping.get(token) == full, f"{token}: {mapping.get(token)}"

    assert len(mapping) == len(expected)
