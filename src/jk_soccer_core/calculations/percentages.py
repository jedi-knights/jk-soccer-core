from typing import Iterable, Optional
from .abstract_match_calculation import AbstractMatchCalculation
from jk_soccer_core import Match

from jk_soccer_core.match import opponent_names_generator, matches_played_generator
from jk_soccer_core.calculations.wins import WinsCalculation
from jk_soccer_core.calculations.losses import LossesCalculation
from jk_soccer_core.calculations.draws import DrawsCalculation


class WinningPercentageCalculation(AbstractMatchCalculation):
    """Calculate the winning percentage for a specific team.

    The tie value is configurable to support multiple RPI methodologies:
    - 0.5 (default): traditional NCAA RPI; ECNL; pre-2024 NCAA women's soccer
    - 1/3: NCAA 2024+ women's soccer Element 1 (per CP Thomas spec)
    """

    def __init__(
        self,
        team_name: Optional[str],
        skip_team_name: Optional[str] = None,
        number_of_digits: int = 2,
        tie_value: float = 0.5,
    ):
        self.__team_name = team_name
        self.__skip_team_name = skip_team_name
        self.__number_of_digits = number_of_digits
        self.__tie_value = tie_value

    def calculate(self, matches: Iterable[Match]) -> float:
        """Calculate the winning percentage for a specific team."""
        if not self.__team_name:
            return 0.0

        filtered_matches = list(
            matches_played_generator(self.__team_name, matches, self.__skip_team_name)
        )
        wins = WinsCalculation(self.__team_name).calculate(filtered_matches)
        losses = LossesCalculation(self.__team_name).calculate(filtered_matches)
        draws = DrawsCalculation(self.__team_name).calculate(filtered_matches)
        matches_played = wins + losses + draws

        if matches_played == 0:
            return 0.0

        result = (float(wins) + (float(draws) * self.__tie_value)) / float(
            matches_played
        )
        return round(result, self.__number_of_digits)


class OpponentsWinningPercentageCalculation(AbstractMatchCalculation):
    """Calculate the average winning percentage of a team's opponents.

    For each opponent encounter (weighted by meeting count), the opponent's WP
    is computed with games against the target team excluded — implementing the
    standard NCAA RPI Element 2 opponent-removal logic.
    """

    def __init__(
        self,
        team_name: Optional[str],
        skip_team_name: Optional[str] = None,
        number_of_digits: int = 2,
        tie_value: float = 0.5,
    ):
        self.__team_name = team_name
        self.__skip_team_name = skip_team_name
        self.__number_of_digits = number_of_digits
        self.__tie_value = tie_value

    def calculate(self, matches: Iterable[Match]) -> float:
        """Calculate the winning percentage of the opponents of a specific team."""
        materialized = list(matches)
        count = 0
        accumulator = 0.0
        for opponent_name in opponent_names_generator(self.__team_name, materialized):
            count += 1
            accumulator += WinningPercentageCalculation(
                opponent_name,
                self.__team_name,
                self.__number_of_digits,
                tie_value=self.__tie_value,
            ).calculate(materialized)

        if count == 0:
            return 0.0

        return round(accumulator / float(count), self.__number_of_digits)


class OpponentsOpponentsWinningPercentageCalculation(AbstractMatchCalculation):
    """Calculate the average OWP of a team's opponents (RPI Element 3).

    For each of the team's opponents X, this computes X's own opponents'
    winning percentage — where each opponent-of-X's record excludes games
    against X (not against the original team).
    """

    def __init__(
        self,
        team_name: Optional[str],
        number_of_digits: int = 2,
        tie_value: float = 0.5,
    ):
        self.__team_name = team_name
        self.__number_of_digits = number_of_digits
        self.__tie_value = tie_value

    def calculate(self, matches: Iterable[Match]) -> float:
        """Calculate the OOWP of a specific team."""
        if not self.__team_name:
            return 0.0

        materialized = list(matches)
        count = 0
        accumulator = 0.0
        for opponent_name in opponent_names_generator(self.__team_name, materialized):
            count += 1
            accumulator += OpponentsWinningPercentageCalculation(
                opponent_name,
                None,
                self.__number_of_digits,
                tie_value=self.__tie_value,
            ).calculate(materialized)

        if count == 0:
            return 0.0

        return round(accumulator / float(count), self.__number_of_digits)
