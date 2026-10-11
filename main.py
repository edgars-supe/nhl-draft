import json
from nhlpy import NHLClient

from standings import get_teams
from models import Drafter
from display import print_results


def main():
    client = NHLClient(debug=True)
    teams = get_teams(client)

    with open("draft.json") as f:
        draft = json.load(f)
    drafters = [Drafter(d['player'], {teams[t] for t in d['teams']}) for d in draft]
    print_results(drafters)

if __name__ == '__main__':
    main()
