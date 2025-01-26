from .event import Event
from .team import Team


class Match(Event):
    home: Team
    away: Team
    home_score: int
    away_score: int
