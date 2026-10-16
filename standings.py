import json
from nhlpy.nhl_client import NHLClient

from models import Team

def get_teams(client: NHLClient) -> dict[str, Team]:
    raw = client.standings.league_standings(season='20262027')['standings']
    with open("standings.json", "w") as f:
        json.dump(raw, f)

    return { t['teamAbbrev']['default']: Team(t) for t in raw }
