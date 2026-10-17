from __future__ import annotations

import json

from nhlpy.nhl_client import NHLClient

from generate_html import generate_html
from history import save_history
from models import Drafter
from standings import get_teams


def main() -> None:
    client: NHLClient = NHLClient(debug=True)
    teams: dict[str, Team] = get_teams(client)

    with open("draft.json") as f:
        draft: list[dict[str, Any]] = json.load(f)
    drafters: list[Drafter] = [Drafter(d['player'], {teams[t] for t in d['teams']}) for d in draft]
    save_history(drafters)
    generate_html(drafters)


if __name__ == '__main__':
    main()
