"""Define environnemental variables for paths"""
import os
from pathlib import Path

PARENT_DIR = Path(__file__).parent.resolve().parent
DATA_DIR = PARENT_DIR / "data"

if not Path(DATA_DIR).exists():
    os.mkdir(DATA_DIR)
