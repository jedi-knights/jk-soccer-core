from collections.abc import Iterable

from jk_soccer_core import Match
from jk_soccer_core.match import matches_played_generator


class WinsCalculation:
    """
    Calculate the number of wins for a specific team.
    """

    def __init__(self, team_name: str | None, skip_team_name: str | None = None):
        self.__team_name = team_name
        self.__skip_team_name = skip_team_name

    def calculate(self, matches: Iterable[Match]) -> int:
        """
        Calculate the number of wins for a specific team.
        """
        team = self.__team_name
        if not team:
            return 0

        return sum(
            1
            for match in matches_played_generator(
                team, matches, skip_team_name=self.__skip_team_name
            )
            if not match.penalty_shootout
            and (
                (match.home_team == team and match.home_score > match.away_score)
                or (match.away_team == team and match.away_score > match.home_score)
            )
        )
