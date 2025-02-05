import random
import uuid

from datetime import date, time, timedelta
from typing import Optional

from dataclasses import dataclass, field


def generate_id() -> str:
    """
    Generate a unique identifier
    """
    return str(uuid.uuid4())


def generate_date() -> date:
    """
    Generate a random date this year but not in the future and not today
    """
    start_date = date(date.today().year, 1, 1)
    end_date = date.today() - timedelta(days=1)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)


def generate_time() -> time:
    """
    Generate a random time
    """
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return time(hour, minute, second)


@dataclass
class Match:
    home_team: Optional[str] = None
    away_team: Optional[str] = None
    home_score: int = 0
    away_score: int = 0
    id: str = field(default_factory=generate_id)
    date: date = field(default_factory=generate_date)
    time: time = field(default_factory=generate_time)


def is_draw(match: Match) -> bool:
    """
    Check if the match is a draw
    """
    return match.home_score == match.away_score


def winner(match: Match) -> Optional[str]:
    """
    Get the winning team
    """
    if match.home_score > match.away_score:
        return match.home_team

    if match.away_score > match.home_score:
        return match.away_team

    return None


def loser(match: Match) -> Optional[str]:
    """
    Get the losing team
    """
    if match.home_score < match.away_score:
        return match.home_team

    if match.away_score < match.home_score:
        return match.away_team

    return None


def has_team_name(match: Match, team_name: str) -> bool:
    """
    Check if the match contains a specific team name
    """
    return match.home_team == team_name or match.away_team == team_name
