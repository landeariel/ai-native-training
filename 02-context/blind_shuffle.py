"""
Shuffle the 10 Setup 4 summaries into blind labels A-J for grading.

Writes:
  blind_summaries.md  - the summaries under labels A-J only (no model, no run, no word count)
  blind_key.json      - which label is which model and run. NOT printed. Don't open it until grading is done.

    01-tokens/.venv/bin/python 02-context/blind_shuffle.py
"""

import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).parent
RUNS_FILE = HERE / "runs_setup4.json"
KEY_FILE = HERE / "blind_key.json"
BLIND_FILE = HERE / "blind_summaries.md"

if KEY_FILE.exists():
    sys.exit(f"{KEY_FILE.name} already exists; not reshuffling.")

runs = json.loads(RUNS_FILE.read_text())
random.SystemRandom().shuffle(runs)  # unpredictable order
labels = "ABCDEFGHIJ"

key = {label: {"model": r["model"], "run": r["run"]} for label, r in zip(labels, runs)}
KEY_FILE.write_text(json.dumps(key, indent=2))

lines = ["# Setup 4: blind summaries", "",
         "Model and run are hidden. A-D are for hand grading.", ""]
for label, r in zip(labels, runs):
    lines += [f"## Summary {label}", "", r["summary"], ""]
BLIND_FILE.write_text("\n".join(lines))
print(f"Shuffled {len(runs)} summaries into {BLIND_FILE.name}. Key saved to {KEY_FILE.name} (not shown).")
