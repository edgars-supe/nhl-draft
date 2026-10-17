from __future__ import annotations

from typing import Any


class Team:
    def __init__(self, data: dict[str, Any]) -> None:
        self.name: str = data['teamName']['default']
        self.common_name: str = data.get('teamCommonName', {}).get('default', self.name)
        self.abbrev: str = data['teamAbbrev']['default']
        self.points: int = data['points']
        self.wins: int = data['wins']
        self.losses: int = data['losses']
        self.ot_losses: int = data.get('otLosses', 0)
        self.games_played: int = data['gamesPlayed']
        self.goal_for: int = data['goalFor']
        self.goal_against: int = data['goalAgainst']
        self.goal_differential: int = data.get('goalDifferential', 0)
        self.logo: str = data.get('teamLogo', '')
        self.division: str = data.get('divisionName', '')
        self.conference: str = data.get('conferenceName', '')


class Drafter:
    def __init__(self, n: str, t: set[Team]) -> None:
        self.name: str = n
        self.teams: set[Team] = t
