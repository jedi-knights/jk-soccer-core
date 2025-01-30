from typing import Iterable, Optional
from .match import MatchCalculation
from jk_soccer_core.models import Match


class LossesCalculation(MatchCalculation):
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
            loser = match.loser()
            if loser is not None and loser.name == team_name:
                count += 1

        return count
