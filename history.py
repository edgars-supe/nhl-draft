import json
import os
from datetime import datetime, timezone


HISTORY_DIR = "results"
HISTORY_FILE = os.path.join(HISTORY_DIR, "history.json")


def save_history(drafters):
    """Save a daily snapshot of drafter points.

    Each day gets one entry; multiple runs on the same day
    overwrite the previous entry for that day.
    """
    os.makedirs(HISTORY_DIR, exist_ok=True)

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    entries = load_history()

    # Replace or append
    found = False
    for entry in entries:
        if entry["date"] == today:
            entry["drafters"] = _snapshot(drafters)
            found = True
            break

    if not found:
        entries.append({
            "date": today,
            "drafters": _snapshot(drafters),
        })

    # Sort by date
    entries.sort(key=lambda e: e["date"])

    with open(HISTORY_FILE, "w") as f:
        json.dump(entries, f, indent=2)


def load_history():
    """Load history entries, sorted by date."""
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE) as f:
        return json.load(f)


def _snapshot(drafters):
    return sorted(
        [{"name": d.name, "points": sum(t.points for t in d.teams)} for d in drafters],
        key=lambda x: x["points"],
        reverse=True,
    )
