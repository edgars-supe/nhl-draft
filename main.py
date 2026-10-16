import json
from nhlpy.nhl_client import NHLClient

from standings import get_teams
from models import Drafter
from html_output import generate_html
from history import save_history


def main():
    client = NHLClient(debug=True)
    teams = get_teams(client)

    with open("draft.json") as f:
        draft = json.load(f)
    drafters = [Drafter(d['player'], {teams[t] for t in d['teams']}) for d in draft]
    save_history(drafters)
    generate_html(drafters)

if __name__ == '__main__':
    main()
