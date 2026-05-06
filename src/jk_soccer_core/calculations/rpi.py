"""Rating Percentage Index (RPI) calculation.

Implements the standard NCAA RPI three-element formula with configurable
weights and tie values. Defaults match the current (2024+) NCAA Division I
women's soccer specification:

- Weights (1, 2, 1)/4 — i.e., 0.25 / 0.50 / 0.25.
- Element 1 (own winning percentage) ties count as 1/3 of a win.
- Element 2 and Element 3 (opponent-record-based) ties count as 1/2 of a win.

To compute the pre-2024 ("traditional") formula, pass ``e1_tie_value=0.5``.
Other methodologies are reachable by overriding ``weights`` and the two
tie-value parameters.

Reference: https://sites.google.com/site/rpifordivisioniwomenssoccer
"""

from collections.abc import Iterable
from dataclasses import dataclass

from jk_soccer_core.calculations.percentages import (
    OpponentsOpponentsWinningPercentageCalculation,
    OpponentsWinningPercentageCalculation,
    WinningPercentageCalculation,
    build_team_index,
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


class RPICalculation:
    """Compute the Rating Percentage Index for a specific team.

    Defaults follow the 2024+ NCAA Division I women's soccer methodology
    (CP Thomas reference): E1 ties = 1/3, E2/E3 ties = 1/2, weights 1:2:1.

    Args:
        team_name: Team to rate. Returns a zero breakdown if empty.
        number_of_digits: Rounding precision for all returned values.
        weights: Three weights ``(w1, w2, w3)`` applied to (E1, E2, E3).
            Divisor is the sum of weights. Defaults to ``(1.0, 2.0, 1.0)``
            which yields the canonical 0.25/0.50/0.25 NCAA formula.
        e1_tie_value: Tie weight for Element 1 (own WP). Defaults to ``1/3``
            (NCAA 2024+ women's soccer). Pass ``0.5`` for the pre-2024
            ("traditional") formula.
        e2_e3_tie_value: Tie weight for Element 2 and Element 3. Defaults
            to 0.5 — NCAA standard for opponent records, which did not
            change in 2024.
    """

    def __init__(
        self,
        team_name: str | None,
        number_of_digits: int = 2,
        weights: tuple[float, float, float] = (1.0, 2.0, 1.0),
        e1_tie_value: float = 1 / 3,
        e2_e3_tie_value: float = 0.5,
    ):
        self.__team_name = team_name
        self.__number_of_digits = number_of_digits
        self.__weights = weights
        self.__e1_tie_value = e1_tie_value
        self.__e2_e3_tie_value = e2_e3_tie_value

    def calculate(self, matches: Iterable[Match]) -> RPIBreakdown:
        """Calculate the RPI breakdown for the configured team.

        All elements are computed at full precision and rounded only at the
        boundary, so per-element rounding does not propagate into composite
        values.

        Returns:
            An ``RPIBreakdown`` with WP, OWP, OOWP, and the composite RPI.
            All values are zero when the team is missing or has no matches.
        """
        if not self.__team_name:
            return _ZERO_BREAKDOWN

        materialized = list(matches)
        if not materialized:
            return _ZERO_BREAKDOWN

        index = build_team_index(materialized)

        wp_raw = WinningPercentageCalculation(
            self.__team_name,
            None,
            self.__number_of_digits,
            tie_value=self.__e1_tie_value,
        )._compute_indexed(index)

        owp_raw = OpponentsWinningPercentageCalculation(
            self.__team_name,
            self.__number_of_digits,
            tie_value=self.__e2_e3_tie_value,
        )._compute_indexed(index)

        oowp_raw = OpponentsOpponentsWinningPercentageCalculation(
            self.__team_name,
            self.__number_of_digits,
            tie_value=self.__e2_e3_tie_value,
        )._compute_indexed(index)

        w1, w2, w3 = self.__weights
        divisor = w1 + w2 + w3
        rpi_raw = (w1 * wp_raw + w2 * owp_raw + w3 * oowp_raw) / divisor

        n = self.__number_of_digits
        return RPIBreakdown(
            wp=round(wp_raw, n),
            owp=round(owp_raw, n),
            oowp=round(oowp_raw, n),
            rpi=round(rpi_raw, n),
        )

    @classmethod
    def calculate_for_all(
        cls,
        matches: Iterable[Match],
        *,
        number_of_digits: int = 2,
        weights: tuple[float, float, float] = (1.0, 2.0, 1.0),
        e1_tie_value: float = 1 / 3,
        e2_e3_tie_value: float = 0.5,
    ) -> dict[str, RPIBreakdown]:
        """Compute the RPI breakdown for every team in ``matches``.

        Builds the team index once and memoizes each team's OWP across the
        full league, so each team's OOWP is composed from cached OWPs rather
        than recomputing them per opponent. Per-element rounding is still
        applied only at the boundary.

        Returns a mapping ``team_name -> RPIBreakdown`` covering every team
        that appears in at least one match. Returns an empty dict when
        ``matches`` is empty.
        """
        materialized = list(matches)
        if not materialized:
            return {}

        index = build_team_index(materialized)
        if not index:
            return {}

        n = number_of_digits

        owp_cache: dict[str, float] = {}

        def owp_raw(team: str) -> float:
            if team not in owp_cache:
                owp_cache[team] = OpponentsWinningPercentageCalculation(
                    team, n, tie_value=e2_e3_tie_value
                )._compute_indexed(index)
            return owp_cache[team]

        w1, w2, w3 = weights
        divisor = w1 + w2 + w3

        results: dict[str, RPIBreakdown] = {}
        for team, team_matches in index.items():
            wp_raw = WinningPercentageCalculation(
                team, None, n, tie_value=e1_tie_value
            )._compute_indexed(index)

            owp = owp_raw(team)

            encounters: dict[str, int] = {}
            for m in team_matches:
                opponent = m.away_team if m.home_team == team else m.home_team
                if opponent is not None:
                    encounters[opponent] = encounters.get(opponent, 0) + 1

            if encounters:
                total = 0
                weighted = 0.0
                for opponent, count in encounters.items():
                    weighted += owp_raw(opponent) * count
                    total += count
                oowp = weighted / float(total)
            else:
                oowp = 0.0

            rpi_raw = (w1 * wp_raw + w2 * owp + w3 * oowp) / divisor
            results[team] = RPIBreakdown(
                wp=round(wp_raw, n),
                owp=round(owp, n),
                oowp=round(oowp, n),
                rpi=round(rpi_raw, n),
            )

        return results
