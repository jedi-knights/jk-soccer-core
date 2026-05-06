from collections.abc import Iterable

from jk_soccer_core import Match
from jk_soccer_core.match import matches_played_generator


class PointsCalculation:
    """
    Calculate the number of points a team has earned in an iterable of matches.
    """

    def __init__(self, team_name: str | None, skip_team_name: str | None = None):
        self.__team_name = team_name
        self.__skip_team_name = skip_team_name

    def calculate(self, matches: Iterable[Match]) -> int:
        """
        Calculate the number of points a team has earned in a list of matches.

        In a match a team earns 1 point if the match is a draw, 0 points if the team lost, and 3 points if the team won.

        :param team_name: The name of the team to calculate the points for.
        :param matches: A list of matches to calculate the points from.
        :return: The number of points the team has earned.
        """
        team = self.__team_name
        if not team:
            return 0

        points = 0
        for match in matches_played_generator(team, matches, self.__skip_team_name):
            if match.penalty_shootout or match.home_score == match.away_score:
                points += 1
            elif (match.home_team == team and match.home_score > match.away_score) or (
                match.away_team == team and match.away_score > match.home_score
            ):
                points += 3

        return points
