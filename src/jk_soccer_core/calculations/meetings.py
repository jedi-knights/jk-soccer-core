from typing import Iterable, Optional
from .match import MatchCalculation
from jk_soccer_core.models import Match, has_team_name


class MeetingsCalculation(MatchCalculation):
    """
    Calculate the number of meetings between two teams.
    """

    def __init__(self, team_name1: Optional[str], team_name2: Optional[str]):
        self.__team_name1 = team_name1
        self.__team_name2 = team_name2

    def calculate(self, matches: Iterable[Match]) -> int:
        """
        Calculate the number of meetings between two teams.

        :param matches: The list of matches to analyze.
        :return: The number of meetings between the two teams.
        """
        meetings = 0
        for match in matches:
            if not has_team_name(match, self.__team_name1):
                continue

            if not has_team_name(match, self.__team_name2):
                continue

            meetings += 1

        return meetings
