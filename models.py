class Team:
    def __init__(self, data):
        self.name = data['teamName']['default']
        self.abbrev = data['teamAbbrev']['default']
        self.points = data['points']
        self.wins = data['wins']
        self.losses = data['losses']
        self.gamesPlayed = data['gamesPlayed']
        self.goalFor = data['goalFor']
        self.goalAgainst = data['goalAgainst']
        self.pointPctg = data['pointPctg']
        self.winPctg = data['winPctg']


class Drafter:
    def __init__(self, n: str, t: set[Team]):
        self.name = n
        self.teams = t
