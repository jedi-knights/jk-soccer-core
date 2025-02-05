from typing import Iterable, Optional
from .match import MatchCalculation
from jk_soccer_core.models import Match, has_team_name, loser


class LossesCalculation(MatchCalculation):
    def __init__(self, team_name: Optional[str]):
        self.__team_name = team_name

    def calculate(self, matches: Iterable[Match]) -> int:
        if self.__team_name is None:
            return 0

        if self.__team_name == "":
            return 0

        count = 0
        for match in matches:
            if not has_team_name(match, self.__team_name):
                continue

            # If we get to this point we know that the team is in the match
            target_name = loser(match)
            if target_name is not None and target_name == self.__team_name:
                count += 1

        return count
