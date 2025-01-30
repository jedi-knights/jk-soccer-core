from typing import Iterable, Optional
from .match import MatchCalculation
from jk_soccer_core.models import Match


class WinsCalculation(MatchCalculation):
    def calculate(self, team_name: Optional[str], matches: Iterable[Match]) -> int:
        if team_name is None:
            return 0

        if team_name == "":
            return 0

        count = 0
        for match in matches:
            if not match.contains_team(team_name):
                continue

            # If we get to this point we know that the team is in the match
            winner = match.winner()
            if winner is not None and winner.name == team_name:
                count += 1

        return count
