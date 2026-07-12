from validation.stat_key_semantics import (
    canonical_xbh,
    spray_to_second,
    spray_to_third,
    validation_view,
)


def test_xbh_is_authoritative():
    stats = {
        "2B": 14,
        "3B": 6,
        "HR": 2,
        "XBH": 6,
        "LOC_2B": 14,
        "LOC_3B": 6,
    }

    assert canonical_xbh(stats) == 6

    assert spray_to_second(stats) == 14
    assert spray_to_third(stats) == 6

    view = validation_view(stats)

    assert view["XBH"] == 6
    assert view["HR"] == 2

    assert view["SPRAY_2B"] == 14
    assert view["SPRAY_3B"] == 6

    assert view["XBH"] != (
        stats["2B"]
        + stats["3B"]
        + stats["HR"]
    )


def test_loc_keys_win():

    stats = {
        "2B": 99,
        "3B": 88,
        "LOC_2B": 4,
        "LOC_3B": 3,
        "XBH": 2,
    }

    assert spray_to_second(stats) == 4
    assert spray_to_third(stats) == 3


def test_compatibility_fallback():

    stats = {
        "2B": 5,
        "3B": 2,
        "XBH": 1,
    }

    assert spray_to_second(stats) == 5
    assert spray_to_third(stats) == 2
