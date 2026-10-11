import json
import os
import time
from nhlpy import NHLClient

from models import Team

STANDINGS_CACHE = "standings.json"
CACHE_TTL = 3600  # 1 hour


def get_teams(client: NHLClient) -> dict[str, Team]:
    try:
        mtime = os.path.getmtime(STANDINGS_CACHE)
        if time.time() - mtime < CACHE_TTL:
            with open(STANDINGS_CACHE, "r") as f:
                raw = json.load(f)
    except (OSError, FileNotFoundError):
        raw = None

    if raw is None:
        raw = client.standings.league_standings(season='20262027')['standings']
        with open(STANDINGS_CACHE, "w") as f:
            json.dump(raw, f)

    return { t['teamAbbrev']['default']: Team(t) for t in raw }
