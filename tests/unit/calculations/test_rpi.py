"""Tests for the RPI calculation.

Reference: https://sites.google.com/site/rpifordivisioniwomenssoccer (CP Thomas).
"""

import pytest
from jk_soccer_core.models import Match
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


def test_rpi_default_weights_match_traditional_ncaa(small_graph):
    """Default weights (1, 2, 1) divide-by-4 → 0.25/0.50/0.25.

    Team A: 2-0-0 → WP = 1.0
    Opponents: B (1-1, excl A → 1.0), C (1-1, excl A → 1.0) → OWP = 1.0

    OOWP from earlier OOWP test = 0.75
    RPI = (1.0 + 2*1.0 + 0.75) / 4 = 0.9375
    """
    result = RPICalculation("Team A", number_of_digits=4).calculate(small_graph)
    assert result.wp == 1.0
    assert result.owp == 1.0
    assert result.oowp == 0.75
    assert result.rpi == 0.9375


def test_rpi_supports_2024_ncaa_women_soccer_tie_value():
    """E1 uses ties=1/3 in 2024+; E2/E3 still use ties=1/2.

    The CP Thomas spec mandates split tie values across elements.
    We verify the RPI class accepts an `e1_tie_value` distinct from
    the OWP/OOWP tie value.
    """
    matches = [
        Match("Team A", "Team B", 1, 1),  # tie
        Match("Team A", "Team C", 1, 0),  # win
        Match("Team A", "Team D", 0, 1),  # loss
        Match("Team B", "Team C", 1, 0),
        Match("Team B", "Team D", 0, 1),
        Match("Team C", "Team D", 1, 1),  # tie between two of A's opponents
    ]
    # E1 with tie=1/3: (1 + 1/3) / 3 = 4/9 = 0.4444
    result = RPICalculation(
        "Team A",
        number_of_digits=4,
        e1_tie_value=1 / 3,
        e2_e3_tie_value=0.5,
    ).calculate(matches)
    assert result.wp == round(4 / 9, 4)


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
    with pytest.raises((AttributeError, Exception)):
        a.wp = 0.0  # type: ignore[misc]
