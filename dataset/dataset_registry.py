from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SAMPLES = ROOT / "samples"


DATASETS = {
    "gamechanger": SAMPLES / "gamechanger" / "raw",
    "playmaker": SAMPLES / "playmaker" / "raw",
    "iscore": SAMPLES / "iscore" / "raw",
    "mlb": SAMPLES / "mlb" / "raw",
    "mlb_statsapi": SAMPLES / "mlb" / "statsapi" / "raw",
    "mlb_statsapi_expected": SAMPLES / "mlb" / "statsapi" / "expected",
    "college": SAMPLES / "college" / "raw",
    "college_presto": SAMPLES / "college" / "presto" / "raw",
    "college_presto_expected": SAMPLES / "college" / "presto" / "expected",
}