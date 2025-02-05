from typing import Iterable, Optional
from .match import MatchCalculation
from jk_soccer_core.models import Match, has_team_name, is_draw, winner


class PointsCalculation(MatchCalculation):
    def __init__(self, team_name: Optional[str]):
        self.__team_name = team_name

    """
    Calculate the number of points a team has earned in a list of matches.
    """

    def calculate(self, matches: Iterable[Match]) -> int:
        """
        Calculate the number of points a team has earned in a list of matches.

        In a match a team earns 1 point if the match is a draw, 0 points if the team lost, and 3 points if the team won.

        :param team_name: The name of the team to calculate the points for.
        :param matches: A list of matches to calculate the points from.
        :return: The number of points the team has earned.
        """
        if self.__team_name is None:
            return 0

        if self.__team_name == "":
            return 0

        points = 0
        for match in matches:
            if not has_team_name(match, self.__team_name):
                continue

            if is_draw(match):
                points += 1
            elif winner(match) == self.__team_name:
                points += 3

        return points
