from __future__ import annotations

import json
from pathlib import Path

import pytest

from cleaners.college_cleaner import clean_college_text
from detectors.event_detector import detect_event_types
from translators.base_translator import detected_events_to_baseball_event

RAW_DIR = Path("samples/college/presto/raw")
MANIFEST_PATH = Path("samples/college/presto/manifest.json")
TARGET = 0.99


def _fixture_paths() -> list[Path]:
    return sorted(p for p in RAW_DIR.glob("*.txt") if p.is_file())


def test_presto_corpus_eventization_meets_target_when_fixtures_exist():
    """
    Scoped claim: on captured Presto/college fixtures under
    samples/college/presto/raw/, cleaned play lines eventize at >= 99%.
    """

    fixtures = _fixture_paths()
    if not fixtures:
        pytest.skip("No Presto capture fixtures yet")

    total_ok = 0
    total_n = 0
    failures: list[str] = []

    for path in fixtures:
        blocks = clean_college_text(path.read_text(encoding="utf-8"))
        ok = 0
        for block in blocks:
            be = detected_events_to_baseball_event(detect_event_types(block))
            if be is not None:
                ok += 1
            else:
                failures.append(f"{path.name}: {block}")
        total_ok += ok
        total_n += len(blocks)

        rate = (ok / len(blocks)) if blocks else 1.0
        assert rate >= TARGET, (
            f"{path.name}: {ok}/{len(blocks)} = {rate:.2%} < {TARGET:.0%}; "
            f"first misses: {failures[:5]}"
        )

    overall = (total_ok / total_n) if total_n else 1.0
    assert overall >= TARGET, (
        f"corpus {total_ok}/{total_n} = {overall:.2%} < {TARGET:.0%}"
    )

    if MANIFEST_PATH.exists():
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        assert float(manifest.get("accuracy_target", TARGET)) == TARGET


def test_known_college_bunt_single_eventizes():
    """Regression for ESPN/Presto-style 'reached on bunt single' language."""

    line = "A. Guzman reached on bunt single to pitcher."
    be = detected_events_to_baseball_event(detect_event_types(line))
    assert be is not None
    assert be.primary_event.value == "single"
