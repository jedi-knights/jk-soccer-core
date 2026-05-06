"""Rating Percentage Index (RPI) calculation.

Implements the standard NCAA RPI three-element formula with configurable
weights and tie values, supporting:

- Traditional NCAA RPI: weights (1, 2, 1)/4, tie_value 0.5 across all elements.
- NCAA 2024+ women's soccer: weights (1, 2, 1)/4, E1 ties = 1/3, E2/E3 ties = 1/2.
- Custom variants: arbitrary 3-tuple weights.

Reference: https://sites.google.com/site/rpifordivisioniwomenssoccer
"""

from dataclasses import dataclass
from typing import Iterable, Optional

from jk_soccer_core.calculations.abstract_match_calculation import (
    AbstractMatchCalculation,
)
from jk_soccer_core.calculations.percentages import (
    OpponentsOpponentsWinningPercentageCalculation,
    OpponentsWinningPercentageCalculation,
    WinningPercentageCalculation,
)
from jk_soccer_core.models import Match


@dataclass(frozen=True)
class RPIBreakdown:
    """Decomposition of an RPI score into its three NCAA elements.

    Attributes:
        wp: Element 1 — the team's own winning percentage.
        owp: Element 2 — opponents' winning percentage.
        oowp: Element 3 — opponents' opponents' winning percentage.
        rpi: The composite RPI value.
    """

    wp: float
    owp: float
    oowp: float
    rpi: float


_ZERO_BREAKDOWN = RPIBreakdown(wp=0.0, owp=0.0, oowp=0.0, rpi=0.0)


class RPICalculation(AbstractMatchCalculation):
    """Compute the Rating Percentage Index for a specific team.

    Args:
        team_name: Team to rate. Returns a zero breakdown if empty.
        number_of_digits: Rounding precision for all returned values.
        weights: Three weights ``(w1, w2, w3)`` applied to (E1, E2, E3).
            Divisor is the sum of weights. Defaults to ``(1.0, 2.0, 1.0)``
            which yields the classical 0.25/0.50/0.25 NCAA formula.
        e1_tie_value: Tie weight for Element 1 (own WP). Defaults to 0.5.
            Set to ``1/3`` for NCAA 2024+ women's soccer.
        e2_e3_tie_value: Tie weight for Element 2 and Element 3. Defaults
            to 0.5 (NCAA standard for opponent records, which did not change
            in 2024).
    """

    def __init__(
        self,
        team_name: Optional[str],
        number_of_digits: int = 2,
        weights: tuple[float, float, float] = (1.0, 2.0, 1.0),
        e1_tie_value: float = 0.5,
        e2_e3_tie_value: float = 0.5,
    ):
        self.__team_name = team_name
        self.__number_of_digits = number_of_digits
        self.__weights = weights
        self.__e1_tie_value = e1_tie_value
        self.__e2_e3_tie_value = e2_e3_tie_value

    def calculate(self, matches: Iterable[Match]) -> RPIBreakdown:
        """Calculate the RPI breakdown for the configured team.

        Returns:
            An ``RPIBreakdown`` with WP, OWP, OOWP, and the composite RPI.
            All values are zero when the team is missing or has no matches.
        """
        if not self.__team_name:
            return _ZERO_BREAKDOWN

        materialized = list(matches)
        if not materialized:
            return _ZERO_BREAKDOWN

        wp = WinningPercentageCalculation(
            self.__team_name,
            None,
            self.__number_of_digits,
            tie_value=self.__e1_tie_value,
        ).calculate(materialized)

        owp = OpponentsWinningPercentageCalculation(
            self.__team_name,
            None,
            self.__number_of_digits,
            tie_value=self.__e2_e3_tie_value,
        ).calculate(materialized)

        oowp = OpponentsOpponentsWinningPercentageCalculation(
            self.__team_name,
            self.__number_of_digits,
            tie_value=self.__e2_e3_tie_value,
        ).calculate(materialized)

        w1, w2, w3 = self.__weights
        divisor = w1 + w2 + w3
        rpi = round((w1 * wp + w2 * owp + w3 * oowp) / divisor, self.__number_of_digits)

        return RPIBreakdown(wp=wp, owp=owp, oowp=oowp, rpi=rpi)
