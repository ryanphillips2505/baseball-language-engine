"""
Guard: GameChanger readings are frozen.

Every GameChanger sample's full BLE reading (per plate appearance,
game events, aggregate stats and final Opponent IQ stats) must match
the stored baseline exactly. New language support for other platforms
must never change what Opponent IQ reads from GameChanger.

If a GameChanger change is intentional, regenerate with:
    py -m tools.output_snapshot write
and review the baseline diff before committing.
"""

import pytest

from tools.output_snapshot import FROZEN_SAMPLES, diff_against_baseline


@pytest.mark.parametrize("name", sorted(FROZEN_SAMPLES))
def test_gamechanger_reading_is_unchanged(name):
    differences = diff_against_baseline(name)

    assert differences == [], "\n".join(differences[:25])
