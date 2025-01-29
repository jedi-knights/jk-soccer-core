from .event import Event
from .team import Team


class Match(Event):
    home: Team = None
    away: Team = None
    home_score: int = 0
    away_score: int = 0
