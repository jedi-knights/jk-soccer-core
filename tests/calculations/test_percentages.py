import pytest
from jk_soccer_core.models import Match, Team
from jk_soccer_core.calculations.percentages import WinningPercentageCalculation


@pytest.fixture
def teams():
    return {
        "Team A": Team(name="Team A"),
        "Team B": Team(name="Team B"),
        "Team C": Team(name="Team C"),
        "Team D": Team(name="Team D"),
        "Team E": Team(name="Team E"),
        "Team F": Team(name="Team F"),
        "Team G": Team(name="Team G"),
        "Team H": Team(name="Team H"),
        "Team I": Team(name="Team I"),
    }


@pytest.fixture
def matches(teams):
    return [
        Match(home=teams["Team A"], away=teams["Team B"], home_score=1, away_score=0),
        Match(home=teams["Team A"], away=teams["Team C"], home_score=2, away_score=1),
        Match(home=teams["Team A"], away=teams["Team D"], home_score=1, away_score=1),
        Match(home=teams["Team B"], away=teams["Team C"], home_score=2, away_score=1),
        Match(home=teams["Team A"], away=teams["Team B"], home_score=0, away_score=1),
        # Team E wins all matches
        Match(home=teams["Team E"], away=teams["Team F"], home_score=3, away_score=0),
        Match(home=teams["Team E"], away=teams["Team G"], home_score=2, away_score=1),
        # Team F loses all matches
        Match(home=teams["Team F"], away=teams["Team H"], home_score=0, away_score=2),
        Match(home=teams["Team F"], away=teams["Team I"], home_score=1, away_score=3),
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
        Match(home=teams["Team A"], away=teams["Team B"], home_score=1, away_score=1),
        Match(home=teams["Team A"], away=teams["Team C"], home_score=2, away_score=2),
        Match(home=teams["Team A"], away=teams["Team D"], home_score=0, away_score=0),
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
        Match(home=teams["Team A"], away=teams["Team B"], home_score=1, away_score=0),
        Match(home=teams["Team A"], away=teams["Team C"], home_score=2, away_score=1),
        Match(
            home=teams["Team A"], away=teams["Team D"], home_score=1, away_score=1
        ),  # Draw
    ]
    calc = WinningPercentageCalculation("Team A", None, number_of_digits=3)
    assert calc.calculate(matches) == 0.833  # 2 wins, 1 draw
