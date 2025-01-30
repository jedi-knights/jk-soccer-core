import pytest
from jk_soccer_core.models import Match, Team
from jk_soccer_core.calculations.points import PointsCalculation

@pytest.fixture
def team_a():
    return Team(name="Team A")

@pytest.fixture
def team_b():
    return Team(name="Team B")

@pytest.fixture
def team_c():
    return Team(name="Team C")

@pytest.fixture
def matches(team_a, team_b, team_c):
    return [
        Match(home=team_a, away=team_b, home_score=2, away_score=2),  # Draw
        Match(home=team_a, away=team_c, home_score=1, away_score=0),  # Team A wins
        Match(home=team_b, away=team_a, home_score=0, away_score=3),  # Team A wins
        Match(home=team_c, away=team_a, home_score=2, away_score=1),  # Team A loses
    ]

def test_points_calculation_team_a(matches, team_a):
    calc = PointsCalculation()
    assert calc.calculate(team_a.name, matches) == 7  # 2 wins (6 points) + 1 draw (1 point)

def test_points_calculation_team_b(matches, team_b):
    calc = PointsCalculation()
    assert calc.calculate(team_b.name, matches) == 1  # 1 draw (1 point)

def test_points_calculation_team_c(matches, team_c):
    calc = PointsCalculation()
    assert calc.calculate(team_c.name, matches) == 3 # 1 win (3 points)

def test_points_calculation_empty_team_name(matches):
    calc = PointsCalculation()
    assert calc.calculate("", matches) == 0

def test_points_calculation_none_team_name(matches):
    calc = PointsCalculation()
    assert calc.calculate(None, matches) == 0

def test_points_calculation_empty_matches(team_a):
    calc = PointsCalculation()
    assert calc.calculate(team_a.name, []) == 0

def test_points_calculation_no_teams():
    match = Match(home=None, away=None, home_score=1, away_score=1)
    calc = PointsCalculation()
    assert calc.calculate("Team A", [match]) == 0
