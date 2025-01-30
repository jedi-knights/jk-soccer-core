from typing import Optional

from .event import Event
from .team import Team


class Match(Event):
    home: Optional[Team] = None
    away: Optional[Team] = None
    home_score: Optional[int] = 0
    away_score: Optional[int] = 0

    def contains_team(self, team_name: Optional[str]) -> bool:
        """
        Check if the match contains a specific team
        """
        if team_name is None:
            return False

        if team_name == "":
            return False

        if self.home is not None:
            if self.home.name == team_name:
                return True

        if self.away is not None:
            if self.away.name == team_name:
                return True

        return False

    def is_draw(self) -> bool:
        """
        Check if the match is a draw
        """
        return self.home_score == self.away_score

    def winner(self) -> Optional[Team]:
        """
        Get the winning team
        """
        if self.home is None or self.away is None:
            return None

        if self.home_score > self.away_score:
            return self.home

        if self.away_score > self.home_score:
            return self.away

        return None

    def loser(self) -> Optional[Team]:
        """
        Get the losing team
        """
        if self.home is None or self.away is None:
            return None

        if self.home_score < self.away_score:
            return self.home

        if self.away_score < self.home_score:
            return self.away

        return None
