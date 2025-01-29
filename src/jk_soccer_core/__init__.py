from typing import List

from jk_soccer_core.models import Match

def main() -> None:
    print("Hello from jk-soccer-core!")

def wins(team_name: str, matches: List[Match]) -> int:
    return sum(
        1
        for match in matches
        if match.home_team == team_name and match.home_score > match.away_score
        or match.away_team == team_name and match.away_score > match.home_score
    )

def losses(team_name: str, matches: List[Match]) -> int:
    return sum(
        1
        for match in matches
        if match.home_team == team_name and match.home_score < match.away_score
        or match.away_team == team_name and match.away_score < match.home_score
    )

def draws(team_name: str, matches: List[Match]) -> int:
    return sum(
        1
        for match in matches
        if match.home_team == team_name and match.home_score == match.away_score
        or match.away_team == team_name and match.away_score == match.home_score
    )

def points(team_name: str, matches: List[Match]) -> int:
    return wins(team_name, matches) * 3 + draws(team_name, matches)

def goals_for(team_name: str, matches: List[Match]) -> int:
    return sum(
        match.home_score
        for match in matches
        if match.home_team == team_name
    ) + sum(
        match.away_score
        for match in matches
        if match.away_team == team_name
    )

def goals_against(team_name: str, matches: List[Match]) -> int:
    return sum(
        match.away_score
        for match in matches
        if match.home_team == team_name
    ) + sum(
        match.home_score
        for match in matches
        if match.away_team == team_name
    )

def goal_difference(team_name: str, matches: List[Match]) -> int:
    return goals_for(team_name, matches) - goals_against(team_name, matches)

def winning_percentage(team_name: str, matches: List[Match]) -> float:
    return wins(team_name, matches) / len(matches) if matches else 0.0
