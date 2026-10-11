import json
from nhlpy import NHLClient


class Team:
    def __init__(self, data):
        self.name = data['teamName']['default']
        self.abbrev = data['teamAbbrev']['default']
        self.points = data['points']

class Drafter:
    def __init__(self, n: str, t: set[Team]):
        self.name = n
        self.teams = t

def main():
    client = NHLClient(debug=True)
    with open("draft.json", "r") as file:
        draft = json.load(file)

    standings = client.standings.league_standings(season='20262027')['standings']
    teams = { team['teamAbbrev']['default']: Team(team) for team in standings }

    drafters: list[Drafter] = []
    for drafter in draft:
        drafter_teams = { teams[team] for team in drafter['teams'] }
        drafters.append(Drafter(drafter['player'], drafter_teams))

    print_results(drafters)

def print_results(drafters: list[Drafter]):
    drafters.sort(key=lambda x: sum(team.points for team in x.teams), reverse=True)

    for drafter in drafters:
        print(f'{drafter.name}: {sum(team.points for team in drafter.teams)} pts')


if __name__ == '__main__':
    main()
