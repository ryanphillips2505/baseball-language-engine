from __future__ import annotations


"""
BLE VALIDATION SEMANTICS
========================

IMPORTANT

BLE itself understands the difference between:

    DOUBLE
    TRIPLE

and:

    LOC_2B
    LOC_3B

Opponent IQ historically reuses the labels "2B" and "3B"
in some compatibility layers.

Therefore:

    XBH must always come from canonical XBH.

    LOC_2B and LOC_3B represent spray locations.

Local validation tools must NEVER assume:

    XBH = 2B + 3B + HR

This module exists only for local validation, replay,
audits, and debugging.

It does NOT change parser behavior.
It does NOT change aggregation behavior.
It does NOT change GameChanger.
"""


def _safe_int(value) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def canonical_xbh(stats: dict | None) -> int:
    """
    Return authoritative XBH.

    Never rebuild from 2B/3B/HR.
    """
    return _safe_int((stats or {}).get("XBH"))


def canonical_hr(stats: dict | None) -> int:
    """
    Return authoritative HR.
    """
    return _safe_int((stats or {}).get("HR"))


def spray_to_second(stats: dict | None) -> int:
    """
    Prefer LOC_2B.

    Fall back to 2B only for compatibility.
    """
    stats = stats or {}

    if "LOC_2B" in stats:
        return _safe_int(stats["LOC_2B"])

    return _safe_int(stats.get("2B"))


def spray_to_third(stats: dict | None) -> int:
    """
    Prefer LOC_3B.

    Fall back to 3B only for compatibility.
    """
    stats = stats or {}

    if "LOC_3B" in stats:
        return _safe_int(stats["LOC_3B"])

    return _safe_int(stats.get("3B"))


def validation_view(stats: dict | None) -> dict[str, int]:
    """
    Produce an unambiguous local validation view.
    """
    stats = stats or {}

    return {
        "BIP": _safe_int(stats.get("BIP")),
        "GB": _safe_int(stats.get("GB")),
        "FB": _safe_int(stats.get("FB")),
        "BUNT": _safe_int(stats.get("BUNT")),
        "XBH": canonical_xbh(stats),
        "HR": canonical_hr(stats),
        "SPRAY_2B": spray_to_second(stats),
        "SPRAY_3B": spray_to_third(stats),
        "K": _safe_int(stats.get("K")),
        "BB": _safe_int(stats.get("BB")),
        "HBP": _safe_int(stats.get("HBP")),
        "SB": _safe_int(stats.get("SB")),
        "CS": _safe_int(stats.get("CS")),
    }
