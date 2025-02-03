from typing import Iterable, Optional
from .match import MatchCalculation
from jk_soccer_core.models import Match


class WinsCalculation(MatchCalculation):
    """
    Calculate the number of wins for a specific team.
    """

    def __init__(self, team_name: Optional[str]):
        self.__team_name = team_name

    def calculate(self, matches: Iterable[Match]) -> int:
        """
        Calculate the number of wins for a specific team.
        """
        if self.__team_name is None:
            return 0

        if self.__team_name == "":
            return 0

        count = 0
        for match in matches:
            if not match.contains_team_name(self.__team_name):
                continue

            # If we get to this point we know that the team is in the match
            winner = match.winner()
            if winner is not None and winner.name == self.__team_name:
                count += 1

        return count
