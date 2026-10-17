from __future__ import annotations

import json
import os
from datetime import datetime, timezone

from models import Drafter

HISTORY_DIR: str = "results"
HISTORY_FILE: str = os.path.join(HISTORY_DIR, "history.json")


def save_history(drafters: list[Drafter]) -> None:
    """Save a daily snapshot of drafter points.

    Each day gets one entry; multiple runs on the same day
    overwrite the previous entry for that day.
    """
    os.makedirs(HISTORY_DIR, exist_ok=True)

    today: str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    entries: list[dict[str, Any]] = load_history()

    # Replace or append
    found: bool = False
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


def load_history() -> list[dict[str, Any]]:
    """Load history entries, sorted by date."""
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE) as f:
        return json.load(f)


def _snapshot(drafters: list[Drafter]) -> list[dict[str, Any]]:
    return sorted(
        [{"name": d.name, "points": sum(t.points for t in d.teams)} for d in drafters],
        key=lambda x: x["points"],
        reverse=True,
    )
