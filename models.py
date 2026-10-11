class Team:
    def __init__(self, data):
        self.name = data['teamName']['default']
        self.abbrev = data['teamAbbrev']['default']
        self.points = data['points']


class Drafter:
    def __init__(self, n: str, t: set[Team]):
        self.name = n
        self.teams = t
