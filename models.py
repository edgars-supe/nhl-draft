class Team:
    def __init__(self, data):
        self.name = data['teamName']['default']
        self.common_name = data.get('teamCommonName', {}).get('default', self.name)
        self.abbrev = data['teamAbbrev']['default']
        self.points = data['points']
        self.wins = data['wins']
        self.losses = data['losses']
        self.ot_losses = data.get('otLosses', 0)
        self.games_played = data['gamesPlayed']
        self.goal_for = data['goalFor']
        self.goal_against = data['goalAgainst']
        self.goal_differential = data.get('goalDifferential', 0)
        self.point_pctg = data['pointPctg']
        self.win_pctg = data['winPctg']
        self.logo = data.get('teamLogo', '')
        self.division = data.get('divisionName', '')
        self.conference = data.get('conferenceName', '')


class Drafter:
    def __init__(self, n: str, t: set[Team]):
        self.name = n
        self.teams = t
