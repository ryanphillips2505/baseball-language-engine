from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SAMPLES = ROOT / "samples"


DATASETS = {
    "gamechanger": SAMPLES / "gamechanger" / "raw",
    "playmaker": SAMPLES / "playmaker" / "raw",
    "iscore": SAMPLES / "iscore" / "raw",
    "mlb": SAMPLES / "mlb" / "raw",
    "college": SAMPLES / "college" / "raw",
}