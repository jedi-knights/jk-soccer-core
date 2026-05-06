import pytest
from jk_soccer_core.models import Match
from jk_soccer_core.calculations.percentages import (
    OpponentsOpponentsWinningPercentageCalculation,
    OpponentsWinningPercentageCalculation,
    WinningPercentageCalculation,
    build_team_index,
)


@pytest.fixture
def teams():
    return (
        "Team A",
        "Team B",
        "Team C",
        "Team D",
        "Team E",
        "Team F",
        "Team G",
        "Team H",
        "Team I",
    )


@pytest.fixture
def matches(teams):
    team_a, team_b, team_c, team_d, team_e, team_f, team_g, team_h, team_i = teams
    return [
        Match(team_a, team_b, 1, 0),
        Match(team_a, team_c, 2, 1),
        Match(team_a, team_d, 1, 1),
        Match(team_b, team_c, 2, 1),
        Match(team_a, team_b, 0, 1),
        # Team E wins all matches
        Match(team_e, team_f, 3, 0),
        Match(team_e, team_g, 2, 1),
        # Team F loses all matches
        Match(team_f, team_h, 0, 2),
        Match(team_f, team_i, 1, 3),
    ]


def test_winning_percentage_calculation_no_team_name(matches):
    calc = WinningPercentageCalculation(None, None)
    assert calc.calculate(matches) == 0.0


def test_winning_percentage_calculation_empty_team_name(matches):
    calc = WinningPercentageCalculation("", None)
    assert calc.calculate(matches) == 0.0


def test_winning_percentage_calculation_all_wins(matches):
    calc = WinningPercentageCalculation("Team E", None)
    assert calc.calculate(matches) == 1.0  # 2 wins, 0 draws, 0 losses


def test_winning_percentage_calculation_all_losses(matches):
    calc = WinningPercentageCalculation("Team F", None)
    assert calc.calculate(matches) == 0.0  # 0 wins, 0 draws, 2 losses


def test_winning_percentage_calculation_all_draws(teams):
    matches = [
        Match("Team A", "Team B", 1, 1),
        Match("Team A", "Team C", 2, 2),
        Match("Team A", "Team D", 0, 0),
    ]
    calc = WinningPercentageCalculation("Team A", None)
    assert calc.calculate(matches) == 0.5  # 0 wins, 3 draws


def test_winning_percentage_calculation_no_matches():
    matches = []
    calc = WinningPercentageCalculation("Team A", None)
    assert calc.calculate(matches) == 0.0


def test_winning_percentage_calculation_skip_team_name(matches):
    calc = WinningPercentageCalculation("Team A", "Team B")
    # Skipping the two A-vs-B matches leaves: A vs C (win), A vs D (draw).
    # WP = (1 + 0.5 * 1) / 2 = 0.75
    assert calc.calculate(matches) == 0.75


def test_winning_percentage_calculation_rounding(teams):
    matches = [
        Match("Team A", "Team B", 1, 0),
        Match("Team A", "Team C", 2, 1),
        Match("Team A", "Team D", 1, 1),  # Draw
    ]
    calc = WinningPercentageCalculation("Team A", None, number_of_digits=3)
    assert calc.calculate(matches) == 0.833  # 2 wins, 1 draw


def test_winning_percentage_calculation_tie_value_one_third():
    """Ties weighted at 1/3 (NCAA 2024 women's soccer rule for E1)."""
    matches = [
        Match("Team A", "Team B", 1, 1),
        Match("Team A", "Team C", 2, 2),
        Match("Team A", "Team D", 0, 0),
    ]
    calc = WinningPercentageCalculation(
        "Team A", None, tie_value=1 / 3, number_of_digits=4
    )
    assert calc.calculate(matches) == round(1 / 3, 4)


def test_winning_percentage_calculation_tie_value_one_third_mixed_record():
    """8-8-4 under 2024 rule: (8 + 4/3)/20 = 0.4667."""
    matches = (
        [Match("Team A", f"W{i}", 1, 0) for i in range(8)]
        + [Match("Team A", f"L{i}", 0, 1) for i in range(8)]
        + [Match("Team A", f"T{i}", 1, 1) for i in range(4)]
    )
    calc = WinningPercentageCalculation(
        "Team A", None, tie_value=1 / 3, number_of_digits=4
    )
    assert calc.calculate(matches) == round((8 + 4 / 3) / 20, 4)


def test_opponents_winning_percentage_calculation_no_team_name():
    """
    Test the calculation when no team name is provided.
    """
    # Arrange
    matches = [
        Match("Team A", "Team B", 1, 0),
        Match("Team A", "Team C", 2, 1),
        Match("Team D", "Team E", 1, 1),
    ]
    calc = OpponentsWinningPercentageCalculation(None)

    # Act
    result = calc.calculate(matches)

    # Assert
    assert result == 0.0


def test_opponents_winning_percentage_calculation_empty_team_name():
    """
    Test the calculation when an empty team name is provided.
    """
    # Arrange
    matches = [
        Match("Team A", "Team B", 1, 0),
        Match("Team A", "Team C", 2, 1),
        Match("Team D", "Team E", 1, 1),
    ]
    calc = OpponentsWinningPercentageCalculation("")

    # Act
    result = calc.calculate(matches)

    # Assert
    assert result == 0.0


def test_opponents_winning_percentage_calculation_all_wins():
    """
    Test the calculation for a team that wins all matches.
    """
    # Arrange
    matches = [
        Match("Team E", "Team F", 3, 0),
        Match("Team E", "Team G", 2, 1),
        Match("Team F", "Team H", 1, 1),
        Match("Team G", "Team H", 0, 2),
    ]
    calc = OpponentsWinningPercentageCalculation("Team E")

    # Act
    result = calc.calculate(matches)

    # Assert
    assert result == 0.25  # Opponents: Team F (0.0), Team G (1.0)


def test_opponents_winning_percentage_calculation_all_losses():
    """
    Test the calculation for a team that loses all matches.
    """
    # Arrange
    matches = [
        Match("Team F", "Team H", 0, 2),
        Match("Team F", "Team I", 1, 3),
        Match("Team H", "Team I", 2, 2),
        Match("Team G", "Team H", 0, 2),
    ]
    calc = OpponentsWinningPercentageCalculation("Team F")

    # Act
    result = calc.calculate(matches)

    # Assert
    assert result == 0.62  # Opponents: Team H (0.5), Team I (0.5)


def test_opponents_winning_percentage_calculation_no_matches():
    """
    Test the calculation when there are no matches.
    """
    # Arrange
    matches = []
    calc = OpponentsWinningPercentageCalculation("Team A")

    # Act
    result = calc.calculate(matches)

    # Assert
    assert result == 0.0


def test_opponents_winning_percentage_calculation_rounding():
    """
    Test the calculation with rounding to a specified number of digits.
    """
    # Arrange
    matches = [
        Match("Team A", "Team B", 1, 0),
        Match("Team A", "Team C", 2, 1),
        Match("Team A", "Team D", 1, 1),  # Draw
        Match("Team B", "Team C", 0, 2),
        Match("Team C", "Team D", 1, 1),
    ]
    calc = OpponentsWinningPercentageCalculation("Team A", number_of_digits=3)

    # Act
    result = calc.calculate(matches)

    # Assert
    assert result == 0.417  # Opponents: Team B (1.0), Team C (1.0), Team D (0.5)


def test_opponents_winning_percentage_calculation_multiple_games():
    """
    Test the calculation when Team A plays multiple games against an opponent.
    """
    # Arrange
    matches = [
        Match("Team A", "Team B", 1, 0),
        Match("Team A", "Team B", 2, 1),
        Match("Team A", "Team C", 1, 1),
        Match("Team B", "Team C", 0, 2),
        Match("Team C", "Team D", 1, 1),
    ]
    calc = OpponentsWinningPercentageCalculation("Team A")

    # Act
    result = calc.calculate(matches)

    # Assert
    assert result == 0.25  # Opponents: Team B (1.0), Team C (0.5)


def test_opponents_winning_percentage_propagates_tie_value():
    """OWP must propagate tie_value into the inner WP computation."""
    matches = [
        Match("Team A", "Team B", 1, 0),  # B vs A (excluded from B's record)
        Match("Team A", "Team C", 1, 0),  # C vs A (excluded from C's record)
        Match("Team B", "Team C", 1, 1),  # B and C tie
    ]
    # Each opponent of Team A has a single non-A match — a tie.
    # With tie_value=1/3, each opponent's WP = 1/3, so OWP = 1/3.
    calc = OpponentsWinningPercentageCalculation(
        "Team A", number_of_digits=4, tie_value=1 / 3
    )
    assert calc.calculate(matches) == round(1 / 3, 4)


def test_oowp_returns_zero_when_team_name_missing():
    matches = [Match("Team A", "Team B", 1, 0)]
    assert (
        OpponentsOpponentsWinningPercentageCalculation(None).calculate(matches) == 0.0
    )
    assert OpponentsOpponentsWinningPercentageCalculation("").calculate(matches) == 0.0


def test_oowp_returns_zero_when_no_matches():
    calc = OpponentsOpponentsWinningPercentageCalculation("Team A")
    assert calc.calculate([]) == 0.0


def test_owp_returns_zero_when_all_opponents_are_none():
    """OWP must handle matches where the opponent slot is None — covers the
    `if opponent is None: continue` and `if count == 0` defensive paths."""
    matches = [Match("Team A", None, 1, 0)]
    calc = OpponentsWinningPercentageCalculation("Team A")
    assert calc.calculate(matches) == 0.0


def test_oowp_returns_zero_when_all_opponents_are_none():
    """OOWP defensive paths analogous to OWP."""
    matches = [Match("Team A", None, 1, 0)]
    calc = OpponentsOpponentsWinningPercentageCalculation("Team A")
    assert calc.calculate(matches) == 0.0


def test_oowp_basic_two_level_recursion():
    """A's OOWP = average of A's opponents' OWPs.

    Graph:
      A beats B, A beats C
      B beats D
      C beats E
      D beats E

    B's OWP = avg(WP(A excl B), WP(D excl B)) = avg(1.0, 1.0) = 1.0
    C's OWP = avg(WP(A excl C), WP(E excl C)) = avg(1.0, 0.0) = 0.5
    OOWP = (1.0 + 0.5) / 2 = 0.75
    """
    matches = [
        Match("Team A", "Team B", 1, 0),
        Match("Team A", "Team C", 1, 0),
        Match("Team B", "Team D", 1, 0),
        Match("Team C", "Team E", 1, 0),
        Match("Team D", "Team E", 1, 0),
    ]
    calc = OpponentsOpponentsWinningPercentageCalculation("Team A", number_of_digits=4)
    assert calc.calculate(matches) == 0.75


def test_oowp_propagates_tie_value():
    """tie_value must flow through to the innermost WP computation."""
    matches = [
        Match("Team A", "Team B", 1, 0),
        Match("Team A", "Team C", 1, 0),
        Match("Team B", "Team D", 1, 1),  # B vs D ties
        Match("Team C", "Team E", 1, 1),  # C vs E ties
    ]
    # B's opponents: A (excl B → A's other game vs C → won → 1.0), D (excl B → D played only B → 0.0)
    # B's OWP = avg(1.0, 0.0) = 0.5
    # C's opponents: A (excl C → A's other game vs B → won → 1.0), E (excl C → E played only C → 0.0)
    # C's OWP = 0.5
    # OOWP = 0.5
    # tie_value should not change this result (no ties in WP computations after exclusion)
    # but pass tie_value=1/3 to confirm wiring exists
    calc = OpponentsOpponentsWinningPercentageCalculation(
        "Team A", number_of_digits=4, tie_value=1 / 3
    )
    assert calc.calculate(matches) == 0.5


# Lock-in tests: per-element rounding must not be reintroduced.
# Each `_compute(...)` returns the unrounded value (e.g. 1/3 ≈ 0.3333333…),
# while `calculate(...)` rounds at the boundary (e.g. 0.3333). The two values
# differ as floats, so any change that reintroduces rounding inside `_compute`
# would make `_compute(...) == 1/3` fail.


def test_wp_compute_returns_unrounded_value():
    """`WinningPercentageCalculation._compute` returns the raw WP at full
    precision; rounding only happens inside `calculate`."""
    matches = [Match("Team A", "Team B", 1, 1)]  # one tie
    calc = WinningPercentageCalculation("Team A", number_of_digits=4, tie_value=1 / 3)
    assert calc._compute(matches) == 1 / 3
    assert calc.calculate(matches) == round(1 / 3, 4)
    assert calc._compute(matches) != calc.calculate(matches)


def test_owp_compute_averages_unrounded_per_opponent_wp():
    """`OpponentsWinningPercentageCalculation._compute` averages opponent
    WPs at full precision. With tie=1/3 and each opponent having a single
    tie excl. A, every opponent's raw WP is 1/3, so OWP is exactly 1/3.
    Per-opponent rounding would yield ``round(1/3, 4)`` (= 0.3333) instead.
    """
    matches = [
        Match("Team A", "Team B", 1, 0),
        Match("Team A", "Team C", 1, 0),
        Match("Team B", "Team D", 1, 1),  # B's only non-A game: a tie
        Match("Team C", "Team E", 1, 1),  # C's only non-A game: a tie
    ]
    calc = OpponentsWinningPercentageCalculation(
        "Team A", number_of_digits=4, tie_value=1 / 3
    )
    assert calc._compute(matches) == 1 / 3
    assert calc.calculate(matches) == round(1 / 3, 4)
    assert calc._compute(matches) != calc.calculate(matches)


def test_oowp_compute_averages_unrounded_per_opponent_owp():
    """`OpponentsOpponentsWinningPercentageCalculation._compute` averages
    opponent OWPs at full precision. The fixture is constructed so every
    opponent's raw OWP is 1/3, making OOWP raw exactly 1/3. Per-OWP
    rounding inside `_compute` would produce ``round(1/3, 4)`` instead.
    """
    matches = [
        Match("Team A", "Team B", 1, 1),  # tie
        Match("Team A", "Team C", 1, 1),  # tie
        Match("Team B", "Team D", 1, 1),  # tie
        Match("Team C", "Team E", 1, 1),  # tie
        Match("Team D", "Team F", 1, 1),  # tie
        Match("Team E", "Team G", 1, 1),  # tie
    ]
    # With tie=1/3 throughout: every "0-0-1" record gives WP raw = 1/3,
    # so each opponent's OWP raw = 1/3, and OOWP raw = 1/3.
    calc = OpponentsOpponentsWinningPercentageCalculation(
        "Team A", number_of_digits=4, tie_value=1 / 3
    )
    assert calc._compute(matches) == 1 / 3
    assert calc.calculate(matches) == round(1 / 3, 4)
    assert calc._compute(matches) != calc.calculate(matches)


# Lock-in tests against `_compute_indexed` directly. These exist alongside the
# `_compute(...)` lock-ins above to also catch a regression that introduced
# rounding inside `_compute_indexed` only — the path used by
# `RPICalculation.calculate` and `RPICalculation.calculate_for_all`.


def test_wp_compute_indexed_returns_unrounded_value():
    """`_compute_indexed` is the path used by RPI and the batch API; it must
    return the raw WP at full precision."""
    matches = [Match("Team A", "Team B", 1, 1)]
    index = build_team_index(matches)
    calc = WinningPercentageCalculation("Team A", number_of_digits=4, tie_value=1 / 3)
    assert calc._compute_indexed(index) == 1 / 3
    assert calc._compute_indexed(index) != round(1 / 3, 4)


def test_owp_compute_indexed_averages_unrounded_per_opponent_wp():
    """OWP via `_compute_indexed` must average opponent WPs at full
    precision when called against a prebuilt index."""
    matches = [
        Match("Team A", "Team B", 1, 0),
        Match("Team A", "Team C", 1, 0),
        Match("Team B", "Team D", 1, 1),
        Match("Team C", "Team E", 1, 1),
    ]
    index = build_team_index(matches)
    calc = OpponentsWinningPercentageCalculation(
        "Team A", number_of_digits=4, tie_value=1 / 3
    )
    assert calc._compute_indexed(index) == 1 / 3
    assert calc._compute_indexed(index) != round(1 / 3, 4)


def test_oowp_compute_indexed_averages_unrounded_per_opponent_owp():
    """OOWP via `_compute_indexed` must average opponent OWPs at full
    precision when called against a prebuilt index."""
    matches = [
        Match("Team A", "Team B", 1, 1),
        Match("Team A", "Team C", 1, 1),
        Match("Team B", "Team D", 1, 1),
        Match("Team C", "Team E", 1, 1),
        Match("Team D", "Team F", 1, 1),
        Match("Team E", "Team G", 1, 1),
    ]
    index = build_team_index(matches)
    calc = OpponentsOpponentsWinningPercentageCalculation(
        "Team A", number_of_digits=4, tie_value=1 / 3
    )
    assert calc._compute_indexed(index) == 1 / 3
    assert calc._compute_indexed(index) != round(1 / 3, 4)
