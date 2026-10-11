from models import Drafter


def print_results(drafters: list[Drafter]):
    drafters.sort(key=lambda x: sum(team.points for team in x.teams), reverse=True)

    header = f"{'Rank':<6}{'Drafter':<10}{'W-L':<12}{'Teams':<38}{'PTS':>5}"
    separator = "─" * len(header)
    print(header)
    print(separator)

    for i, drafter in enumerate(drafters, 1):
        total = sum(team.points for team in drafter.teams)
        wins = sum(team.wins for team in drafter.teams)
        losses = sum(team.losses for team in drafter.teams)
        team_list = ', '.join(t.abbrev for t in drafter.teams)
        record = f"{wins}-{losses}"
        print(f"{i:<6}{drafter.name:<10}{record:<12}{team_list:<38}{total:>5}")
