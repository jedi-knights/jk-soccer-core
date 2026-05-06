from collections.abc import Iterable

from jk_soccer_core import Match
from jk_soccer_core.match import matches_played_generator


class DrawsCalculation:
    def __init__(self, team_name: str | None, skip_team_name: str | None = None):
        self.__team_name = team_name
        self.__skip_team_name = skip_team_name

    def calculate(self, matches: Iterable[Match]) -> int:
        """
        Calculate the number of draws for a specific team.
        """
        if not self.__team_name:
            return 0

        return sum(
            1
            for match in matches_played_generator(
                self.__team_name, matches, self.__skip_team_name
            )
            if match.penalty_shootout or match.home_score == match.away_score
        )
