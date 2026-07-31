from extractors.player_extractor import extract_batter_name
from assemblers.plate_appearance_builder import build_plate_appearance
from models.types import EventType
from pipeline.process_game import process_game
from pathlib import Path


def test_mlb_overturned_challenge_assigns_actual_batter_not_challenger():
    text = (
        "Shea Langeliers challenged (pitch result), call on the field was "
        "overturned: Nolan Schanuel called out on strikes."
    )

    assert extract_batter_name(text) == "Nolan Schanuel"

    pa = build_plate_appearance(text)
    assert pa.batter_name == "Nolan Schanuel"
    assert pa.baseball_event is not None
    assert pa.baseball_event.primary_event == EventType.STRIKEOUT_LOOKING


def test_mlb_confirmed_challenge_assigns_batter_from_final_call():
    text = (
        "Wade Meckler challenged (pitch result), call on the field was "
        "confirmed: Wade Meckler called out on strikes."
    )

    assert extract_batter_name(text) == "Wade Meckler"


def test_mlb_team_challenge_overturned_caught_stealing_has_no_false_batter_prefix():
    text = (
        "Mariners challenged (tag play), call on the field was overturned: "
        "Wilyer Abreu caught stealing 2nd base, catcher Cal Raleigh to "
        "second baseman Cole Young."
    )

    # Runner-only outcome after the challenge wrapper.
    assert extract_batter_name(text) == "Wilyer Abreu"


def test_mlb_statsapi_challenge_plays_use_matchup_batter_names():
    raw = Path(
        "samples/mlb/statsapi/raw/"
        "mlb_angels_athletics_2026_06_20_gamepk824988.live.json"
    ).read_text(encoding="utf-8")

    game = process_game(raw)

    matching = [
        pa
        for pa in game.plate_appearances
        if pa.batter_name == "Nolan Schanuel"
        and pa.baseball_event
        and pa.baseball_event.primary_event == EventType.STRIKEOUT_LOOKING
    ]

    assert matching, "Expected Nolan Schanuel overturned called strikeout"

    challenger_pas = [
        pa
        for pa in game.plate_appearances
        if pa.batter_name is not None
        and "challenged" in pa.batter_name.lower()
    ]
    assert challenger_pas == []
