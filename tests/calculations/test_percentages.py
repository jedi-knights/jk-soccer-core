import pytest
from jk_soccer_core.models import Match
from jk_soccer_core.calculations.percentages import WinningPercentageCalculation


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
    assert (
        calc.calculate(matches) == 0.75
    )  # 2 wins, 1 draw, 1 loss (skipping matches with Team B)


def test_winning_percentage_calculation_rounding(teams):
    matches = [
        Match("Team A", "Team B", 1, 0),
        Match("Team A", "Team C", 2, 1),
        Match("Team A", "Team D", 1, 1),  # Draw
    ]
    calc = WinningPercentageCalculation("Team A", None, number_of_digits=3)
    assert calc.calculate(matches) == 0.833  # 2 wins, 1 draw
