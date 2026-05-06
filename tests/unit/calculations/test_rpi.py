"""Tests for the RPI calculation.

Reference: https://sites.google.com/site/rpifordivisioniwomenssoccer (CP Thomas).
"""

import pytest
from jk_soccer_core.models import Match
from jk_soccer_core.calculations.percentages import (
    OpponentsOpponentsWinningPercentageCalculation,
    OpponentsWinningPercentageCalculation,
    WinningPercentageCalculation,
)
from jk_soccer_core.calculations.rpi import RPICalculation, RPIBreakdown


@pytest.fixture
def small_graph():
    """Five-team graph used in OOWP tests; reused for end-to-end RPI."""
    return [
        Match("Team A", "Team B", 1, 0),
        Match("Team A", "Team C", 1, 0),
        Match("Team B", "Team D", 1, 0),
        Match("Team C", "Team E", 1, 0),
        Match("Team D", "Team E", 1, 0),
    ]


def test_rpi_returns_zero_breakdown_when_team_name_missing():
    matches = [Match("Team A", "Team B", 1, 0)]
    result = RPICalculation(None).calculate(matches)
    assert result == RPIBreakdown(wp=0.0, owp=0.0, oowp=0.0, rpi=0.0)


def test_rpi_returns_zero_breakdown_when_no_matches():
    result = RPICalculation("Team A").calculate([])
    assert result == RPIBreakdown(wp=0.0, owp=0.0, oowp=0.0, rpi=0.0)


def test_rpi_default_weights_yield_canonical_formula(small_graph):
    """Default weights (1, 2, 1) divide-by-4 → 0.25/0.50/0.25.

    Team A: 2-0-0 → WP = 1.0
    Opponents: B (1-0, excl A → 1.0), C (1-0, excl A → 1.0) → OWP = 1.0
    OOWP = 0.75 (B's OWP=1.0, C's OWP=0.5)
    RPI = (1.0 + 2*1.0 + 0.75) / 4 = 0.9375

    No ties, so E1 tie value (1/3 vs 0.5) does not affect the result —
    this exercises the structural formula and weights.
    """
    result = RPICalculation("Team A", number_of_digits=4).calculate(small_graph)
    assert result.wp == 1.0
    assert result.owp == 1.0
    assert result.oowp == 0.75
    assert result.rpi == 0.9375


def test_rpi_default_e1_tie_value_is_2024_ncaa_one_third():
    """The default ``e1_tie_value`` is 1/3 (NCAA 2024+ women's soccer).

    Team A record 1W-1L-1T → WP = (1 + 1/3) / 3 = 4/9 ≈ 0.4444.
    If the default were the pre-2024 0.5, WP would be 0.5 instead.
    """
    matches = [
        Match("Team A", "Team B", 1, 1),  # tie
        Match("Team A", "Team C", 1, 0),  # win
        Match("Team A", "Team D", 0, 1),  # loss
        Match("Team B", "Team C", 1, 0),
        Match("Team B", "Team D", 0, 1),
        Match("Team C", "Team D", 1, 1),
    ]
    result = RPICalculation("Team A", number_of_digits=4).calculate(matches)
    assert result.wp == round(4 / 9, 4)


def test_rpi_pre_2024_traditional_formula_via_explicit_tie_value():
    """Pre-2024 ('traditional') RPI: E1 tie value 0.5 — must opt in explicitly."""
    matches = [
        Match("Team A", "Team B", 1, 1),  # tie
        Match("Team A", "Team C", 1, 0),  # win
        Match("Team A", "Team D", 0, 1),  # loss
        Match("Team B", "Team C", 1, 0),
        Match("Team B", "Team D", 0, 1),
        Match("Team C", "Team D", 1, 1),
    ]
    # E1 with tie=0.5: (1 + 0.5) / 3 = 0.5
    result = RPICalculation(
        "Team A",
        number_of_digits=4,
        e1_tie_value=0.5,
    ).calculate(matches)
    assert result.wp == 0.5


def test_rpi_custom_weights():
    """Weights (1, 1, 1) → simple average of three elements."""
    matches = [
        Match("Team A", "Team B", 1, 0),
        Match("Team A", "Team C", 1, 0),
        Match("Team B", "Team C", 1, 0),
    ]
    # WP(A) = 1.0
    # B's WP excl A: B vs C → 1.0; C's WP excl A: C vs B → 0.0
    # OWP = (1.0 + 0.0)/2 = 0.5
    # B's OWP: opponents A, C
    #   A excl B: A vs C → 1.0; C excl B: C vs A → 0.0; B's OWP = 0.5
    # C's OWP: opponents A, B
    #   A excl C: A vs B → 1.0; B excl C: B vs A → 0.0; C's OWP = 0.5
    # OOWP = 0.5
    # RPI(1,1,1) = (1.0 + 0.5 + 0.5)/3 = 0.6667
    result = RPICalculation(
        "Team A", number_of_digits=4, weights=(1.0, 1.0, 1.0)
    ).calculate(matches)
    assert result.rpi == round((1.0 + 0.5 + 0.5) / 3, 4)


def test_rpi_breakdown_is_immutable_dataclass():
    """RPIBreakdown is a frozen dataclass safe to use as a dict key."""
    a = RPIBreakdown(wp=1.0, owp=0.5, oowp=0.25, rpi=0.5625)
    # Frozen dataclass writes raise FrozenInstanceError, a subclass of AttributeError.
    with pytest.raises(AttributeError):
        a.wp = 0.0  # type: ignore[misc]


def test_rpi_intermediates_are_unrounded_at_the_boundary():
    """Lock in: RPI's WP/OWP/OOWP fields and the composite are derived from
    each percentage class's ``_compute`` (full precision) and rounded only
    at the boundary. If ``RPICalculation`` ever pulled rounded values from
    ``calculate`` again, the composite would diverge from the unrounded
    weighted sum.
    """
    matches = [
        Match("Team A", "Team B", 1, 1),
        Match("Team A", "Team C", 1, 1),
        Match("Team B", "Team D", 1, 1),
        Match("Team C", "Team E", 1, 1),
        Match("Team D", "Team F", 1, 1),
        Match("Team E", "Team G", 1, 1),
    ]
    target = "Team A"
    n = 4
    e1 = 1 / 3
    e23 = 1 / 3

    result = RPICalculation(
        target,
        number_of_digits=n,
        e1_tie_value=e1,
        e2_e3_tie_value=e23,
    ).calculate(matches)

    wp_raw = WinningPercentageCalculation(target, None, n, tie_value=e1)._compute(
        matches
    )
    owp_raw = OpponentsWinningPercentageCalculation(target, n, tie_value=e23)._compute(
        matches
    )
    oowp_raw = OpponentsOpponentsWinningPercentageCalculation(
        target, n, tie_value=e23
    )._compute(matches)

    # Each breakdown field must be the unrounded `_compute` value rounded once.
    assert result.wp == round(wp_raw, n)
    assert result.owp == round(owp_raw, n)
    assert result.oowp == round(oowp_raw, n)

    # The composite must come from the unrounded weighted sum.
    expected_rpi = round((wp_raw + 2 * owp_raw + oowp_raw) / 4, n)
    assert result.rpi == expected_rpi

    # Sanity: the unrounded raw values are *not* equal to their rounded
    # counterparts. If they were, this test wouldn't actually constrain
    # anything — it would pass trivially even with per-element rounding.
    assert wp_raw != round(wp_raw, n)
    assert owp_raw != round(owp_raw, n)
    assert oowp_raw != round(oowp_raw, n)


def test_calculate_for_all_returns_empty_dict_for_empty_matches():
    assert RPICalculation.calculate_for_all([]) == {}


def test_calculate_for_all_matches_per_team_calls(small_graph):
    """Batch ``calculate_for_all`` must produce the same RPIBreakdown for
    every team as calling ``RPICalculation(team).calculate(matches)``
    individually. Locks in zero drift between the two paths."""
    teams = sorted(
        {m.home_team for m in small_graph} | {m.away_team for m in small_graph}
    )

    expected = {
        team: RPICalculation(team, number_of_digits=4).calculate(small_graph)
        for team in teams
        if team is not None
    }
    actual = RPICalculation.calculate_for_all(small_graph, number_of_digits=4)

    assert actual == expected


def test_calculate_for_all_respects_tie_values_and_weights():
    """The classmethod must thread tie values and weights through the same
    way the instance API does — so customising tie values yields identical
    per-team results to the individual path."""
    matches = [
        Match("Team A", "Team B", 1, 1),
        Match("Team A", "Team C", 1, 0),
        Match("Team A", "Team D", 0, 1),
        Match("Team B", "Team C", 1, 0),
        Match("Team B", "Team D", 0, 1),
        Match("Team C", "Team D", 1, 1),
    ]
    teams = ["Team A", "Team B", "Team C", "Team D"]

    expected = {
        team: RPICalculation(
            team,
            number_of_digits=6,
            weights=(1.0, 1.0, 1.0),
            e1_tie_value=0.5,
            e2_e3_tie_value=0.5,
        ).calculate(matches)
        for team in teams
    }
    actual = RPICalculation.calculate_for_all(
        matches,
        number_of_digits=6,
        weights=(1.0, 1.0, 1.0),
        e1_tie_value=0.5,
        e2_e3_tie_value=0.5,
    )
    assert actual == expected


def test_calculate_for_all_excludes_none_team_names():
    """Matches with ``None`` team slots are tolerated; the ``None`` slot is
    not an entry in the returned dict."""
    matches = [
        Match("Team A", "Team B", 1, 0),
        Match("Team A", None, 1, 0),
    ]
    result = RPICalculation.calculate_for_all(matches)
    assert set(result.keys()) == {"Team A", "Team B"}


def test_calculate_for_all_returns_empty_when_all_matches_have_no_teams():
    """If every match has both teams as ``None``, the index is empty and
    no team can be ranked — return ``{}``."""
    matches = [Match(None, None, 1, 0)]
    assert RPICalculation.calculate_for_all(matches) == {}


def test_calculate_for_all_handles_team_with_only_none_opponents():
    """A team whose only match has a ``None`` opponent gets a zero OOWP —
    covers the defensive ``oowp = 0.0`` path when encounters is empty."""
    matches = [Match("Team A", None, 1, 0)]
    result = RPICalculation.calculate_for_all(matches)
    assert "Team A" in result
    assert result["Team A"].oowp == 0.0
