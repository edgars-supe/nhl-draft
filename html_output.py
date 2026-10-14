from datetime import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from models import Drafter, Team
from history import load_history


def _build_drafter(drafter: Drafter) -> dict:
    teams = sorted(drafter.teams, key=lambda t: t.points, reverse=True)
    total = sum(t.points for t in teams)
    wins = sum(t.wins for t in teams)
    losses = sum(t.losses for t in teams)
    ot_losses = sum(t.ot_losses for t in teams)
    return {
        "name": drafter.name,
        "total_points": total,
        "record": f"{wins}-{losses}-{ot_losses}",
        "sorted_teams": [_build_team(t) for t in teams],
    }


def _build_team(team: Team) -> dict:
    return {
        "logo": team.logo,
        "common_name": team.common_name,
        "abbrev": team.abbrev,
        "conference": team.conference,
        "division": team.division,
        "points": team.points,
        "games_played": team.games_played,
        "wins": team.wins,
        "losses": team.losses,
        "ot_losses": team.ot_losses,
        "goal_for": team.goal_for,
        "goal_against": team.goal_against,
        "goal_differential": team.goal_differential,
    }


def generate_html(drafters: list[Drafter], output_file: str = "index.html"):
    env = Environment(
        loader=FileSystemLoader(Path(__file__).parent),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template("standings_template.html")

    data = [_build_drafter(d) for d in drafters]

    cache_file = Path(__file__).parent / "standings.json"
    local_tz = datetime.now().astimezone().tzinfo
    if cache_file.exists():
        mtime = datetime.fromtimestamp(cache_file.stat().st_mtime, tz=local_tz)
    else:
        mtime = datetime.now(local_tz)
    update_time = mtime.strftime("%B %d, %Y at %H:%M %z")

    history = load_history()

    html = template.render(drafters=data, update_time=update_time, history=history)

    with open(output_file, "w") as f:
        f.write(html)

    print(f"Generated {output_file}")
