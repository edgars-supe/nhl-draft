from models import Drafter


def print_results(drafters: list[Drafter]):
    drafters.sort(key=lambda x: sum(team.points for team in x.teams), reverse=True)

    header = f"{'Rank':<6}{'Drafter':<10}{'Teams':<38}{'Points':>7}"
    separator = "─" * len(header)
    print(header)
    print(separator)

    for i, drafter in enumerate(drafters, 1):
        total = sum(team.points for team in drafter.teams)
        team_list = ', '.join(t.abbrev for t in drafter.teams)
        print(f"{i:<6}{drafter.name:<10}{team_list:<38}{total:>7}")
