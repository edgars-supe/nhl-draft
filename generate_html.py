from __future__ import annotations

from datetime import datetime, tzinfo
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader

from history import load_history
from models import Drafter, Team


class StandingsEntry:
    """Represents a row in the standings table."""

    def __init__(self, name: str, total_points: int, record: str, teams: set[Team], games_played: int = 0, points_diff: int = 0) -> None:
        self.name: str = name
        self.total_points: int = total_points
        self.record: str = record
        self.teams: set[Team] = teams
        self.games_played: int = games_played
        self.points_diff: int = points_diff


class GraphDateEntry:
    """Represents a date entry in the points-over-time graph."""

    def __init__(self, date: str, drafters: list[DrafterPoint]) -> None:
        self.date: str = date
        self.drafters: list[DrafterPoint] = drafters


class DrafterDetail:
    """Represents the detailed section for a drafter with all team cards."""

    def __init__(self, name: str, total_points: int, record: str, sorted_teams: list[TeamInfo]) -> None:
        self.name: str = name
        self.total_points: int = total_points
        self.record: str = record
        self.sorted_teams: list[TeamInfo] = sorted_teams


class TeamInfo:
    """Represents team data rendered inside a drafter's detailed section."""

    def __init__(self, team: Team) -> None:
        self.logo: str = team.logo
        self.common_name: str = team.common_name
        self.abbrev: str = team.abbrev
        self.conference: str = team.conference
        self.division: str = team.division
        self.points: int = team.points
        self.games_played: int = team.games_played
        self.wins: int = team.wins
        self.losses: int = team.losses
        self.ot_losses: int = team.ot_losses
        self.goal_for: int = team.goal_for
        self.goal_against: int = team.goal_against
        self.goal_differential: int = team.goal_differential


class DrafterPoint:
    """Represents a single drafter's point snapshot for a graph date entry."""

    CHART_COLORS: list[str] = [
        '#58a6ff', '#f0883e', '#3fb950', '#d2a8ff', '#f85149', '#79c0ff',
    ]

    def __init__(self, name: str, points: int, color: str, points_diff: int = 0) -> None:
        self.name: str = name
        self.points: int = points
        self.color: str = color
        self.points_diff: int = points_diff


def _build_team_info(team: Team) -> TeamInfo:
    return TeamInfo(team)


def _build_standings_entry(drafter: Drafter, history: list[dict[str, Any]]) -> StandingsEntry:
    teams: list[Team] = sorted(drafter.teams, key=lambda t: t.points, reverse=True)
    total: int = sum(t.points for t in teams)
    wins: int = sum(t.wins for t in teams)
    losses: int = sum(t.losses for t in teams)
    ot_losses: int = sum(t.ot_losses for t in teams)
    games_played: int = sum(t.games_played for t in teams)

    points_diff: int = 0
    drafter_points: dict[str, list[int]] = {}
    for entry in history:
        for d in entry["drafters"]:
            drafter_points.setdefault(d["name"], []).append(d["points"])
    points_list = drafter_points.get(drafter.name, [])
    if len(points_list) >= 2:
        points_diff = points_list[-1] - points_list[-2]

    return StandingsEntry(
        name=drafter.name,
        total_points=total,
        record=f"{wins}-{losses}-{ot_losses}",
        teams=drafter.teams,
        games_played=games_played,
        points_diff=points_diff,
    )


def _build_drafter_detail(drafter: Drafter) -> DrafterDetail:
    teams: list[Team] = sorted(drafter.teams, key=lambda t: t.points, reverse=True)
    total: int = sum(t.points for t in teams)
    wins: int = sum(t.wins for t in teams)
    losses: int = sum(t.losses for t in teams)
    ot_losses: int = sum(t.ot_losses for t in teams)
    return DrafterDetail(
        name=drafter.name,
        total_points=total,
        record=f"{wins}-{losses}-{ot_losses}",
        sorted_teams=[TeamInfo(t) for t in teams],
    )


def _build_graph_entries(history: list[dict[str, Any]]) -> list[GraphDateEntry]:
    name_to_index: dict[str, int] = {}
    name_to_color: dict[str, str] = {}
    for i, name in enumerate(
        sorted({d["name"] for entry in history for d in entry["drafters"]})
    ):
        name_to_index[name] = i
        name_to_color[name] = DrafterPoint.CHART_COLORS[i % len(DrafterPoint.CHART_COLORS)]

    # Build a map of drafter name -> list of points across all history entries
    drafter_points_map: dict[str, list[int]] = {}
    for entry in history:
        for d in entry["drafters"]:
            drafter_points_map.setdefault(d["name"], []).append(d["points"])

    result: list[GraphDateEntry] = []
    for entry_idx, entry in enumerate(history):
        drafters: list[DrafterPoint] = []
        for d in entry["drafters"]:
            points_list = drafter_points_map.get(d["name"], [])
            # Compute diff from previous day for THIS entry
            points_diff: int = 0
            if entry_idx > 0:
                prev_points = points_list[entry_idx - 1] if entry_idx - 1 < len(points_list) else None
                curr_points = points_list[entry_idx]
                if prev_points is not None:
                    points_diff = curr_points - prev_points
            drafters.append(
                DrafterPoint(
                    name=d["name"],
                    points=d["points"],
                    color=name_to_color[d["name"]],
                    points_diff=points_diff,
                )
            )
        result.append(GraphDateEntry(date=entry["date"], drafters=drafters))
    return result


def generate_html(drafters: list[Drafter], output_file: str = "index.html") -> None:
    env: Environment = Environment(
        loader=FileSystemLoader(Path(__file__).parent),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    def team_badges(teams: set[Team]) -> str:
        return "".join(
            f'<span class="team-badge">{t.abbrev}</span>'
            for t in teams
        )

    def format_diff(diff: int) -> str:
        if diff > 0:
            return f"+{diff}"
        return str(diff)

    env.filters["team_badges"] = team_badges
    env.filters["format_diff"] = format_diff

    template: Any = env.get_template("standings_template.html")

    history: list[dict[str, Any]] = load_history()

    standings: list[StandingsEntry] = sorted(
        [_build_standings_entry(d, history) for d in drafters],
        key=lambda t: t.total_points,
        reverse=True,
    )

    details: list[DrafterDetail] = sorted(
        [_build_drafter_detail(d) for d in drafters],
        key=lambda t: t.total_points,
        reverse=True,
    )

    graph_entries: list[GraphDateEntry] = _build_graph_entries(history)

    def _serialize_graph_entries(entries: list[GraphDateEntry]) -> list[dict[str, Any]]:
        return [
            {
                "date": e.date,
                "drafters": [
                    {"name": d.name, "points": d.points, "color": d.color, "points_diff": d.points_diff}
                    for d in e.drafters
                ],
            }
            for e in entries
        ]

    cache_file: Path = Path(__file__).parent / "standings.json"
    local_tz: tzinfo | None = datetime.now().astimezone().tzinfo
    if cache_file.exists():
        mtime: datetime = datetime.fromtimestamp(cache_file.stat().st_mtime, tz=local_tz)
    else:
        mtime = datetime.now(local_tz)
    update_time: str = mtime.strftime("%B %d, %Y at %H:%M %z")

    html: str = template.render(
        standings=standings,
        details=details,
        update_time=update_time,
        graph_entries=_serialize_graph_entries(graph_entries),
    )

    with open(output_file, "w") as f:
        f.write(html)

    print(f"Generated {output_file}")
