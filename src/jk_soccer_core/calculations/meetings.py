from collections.abc import Iterable

from jk_soccer_core import Match
from jk_soccer_core.match import meetings_generator


class MeetingsCalculation:
    """
    Calculate the number of meetings between two teams.
    """

    def __init__(self, team_name1: str | None, team_name2: str | None):
        self.__team_name1 = team_name1
        self.__team_name2 = team_name2

    def calculate(self, matches: Iterable[Match]) -> int:
        """
        Calculate the number of meetings between two teams.

        :param matches: The list of matches to analyze.
        :return: The number of meetings between the two teams.
        """
        return sum(
            1 for _ in meetings_generator(self.__team_name1, self.__team_name2, matches)
        )
