import pytest
from jk_soccer_core import wins, losses, draws, points, goals_for, goals_against, goal_difference, winning_percentage
from jk_soccer_core.models import Match

@pytest.fixture
def matches():
    return [
        Match(home_team="Team A", away_team="Team B", home_score=2, away_score=1),
        Match(home_team="Team A", away_team="Team C", home_score=1, away_score=1),
        Match(home_team="Team B", away_team="Team A", home_score=0, away_score=3),
        Match(home_team="Team C", away_team="Team A", home_score=2, away_score=2),
    ]

@pytest.fixture
def empty_matches():
    return []

@pytest.mark.parametrize("team_name, expected", [
    ("Team A", 2),
    ("Team B", 0),
    ("Team C", 0),
])
def test_wins(team_name, expected, matches):
    assert wins(team_name, matches) == expected

@pytest.mark.parametrize("team_name, expected", [
    ("Team A", 0),
    ("Team B", 2),
    ("Team C", 0),
])
def test_losses(team_name, expected, matches):
    assert losses(team_name, matches) == expected

@pytest.mark.parametrize("team_name, expected", [
    ("Team A", 2),
    ("Team B", 0),
    ("Team C", 2),
])
def test_draws(team_name, expected, matches):
    assert draws(team_name, matches) == expected

@pytest.mark.parametrize("team_name, expected", [
    ("Team A", 8),
    ("Team B", 0),
    ("Team C", 2),
])
def test_points(team_name, expected, matches):
    assert points(team_name, matches) == expected

@pytest.mark.parametrize("team_name, expected", [
    ("Team A", 8),
    ("Team B", 1),
    ("Team C", 3),
])
def test_goals_for(team_name, expected, matches):
    assert goals_for(team_name, matches) == expected

@pytest.mark.parametrize("team_name, expected", [
    ("Team A", 4),
    ("Team B", 5),
    ("Team C", 3),
])
def test_goals_against(team_name, expected, matches):
    assert goals_against(team_name, matches) == expected

@pytest.mark.parametrize("team_name, expected", [
    ("Team A", 4),
    ("Team B", -4),
    ("Team C", 0),
])
def test_goal_difference(team_name, expected, matches):
    assert goal_difference(team_name, matches) == expected

@pytest.mark.parametrize("team_name, expected", [
    ("Team A", 0.5),
    ("Team B", 0.0),
    ("Team C", 0.0),
])
def test_winning_percentage(team_name, expected, matches):
    assert winning_percentage(team_name, matches) == expected

@pytest.mark.parametrize("team_name, expected", [
    ("Team A", 0),
])
def test_wins_empty(team_name, expected, empty_matches):
    assert wins(team_name, empty_matches) == expected

@pytest.mark.parametrize("team_name, expected", [
    ("Team A", 0),
])
def test_losses_empty(team_name, expected, empty_matches):
    assert losses(team_name, empty_matches) == expected

@pytest.mark.parametrize("team_name, expected", [
    ("Team A", 0),
])
def test_draws_empty(team_name, expected, empty_matches):
    assert draws(team_name, empty_matches) == expected

@pytest.mark.parametrize("team_name, expected", [
    ("Team A", 0),
])
def test_points_empty(team_name, expected, empty_matches):
    assert points(team_name, empty_matches) == expected

@pytest.mark.parametrize("team_name, expected", [
    ("Team A", 0),
])
def test_goals_for_empty(team_name, expected, empty_matches):
    assert goals_for(team_name, empty_matches) == expected

@pytest.mark.parametrize("team_name, expected", [
    ("Team A", 0),
])
def test_goals_against_empty(team_name, expected, empty_matches):
    assert goals_against(team_name, empty_matches) == expected

@pytest.mark.parametrize("team_name, expected", [
    ("Team A", 0),
])
def test_goal_difference_empty(team_name, expected, empty_matches):
    assert goal_difference(team_name, empty_matches) == expected

@pytest.mark.parametrize("team_name, expected", [
    ("Team A", 0.0),
])
def test_winning_percentage_empty(team_name, expected, empty_matches):
    assert winning_percentage(team_name, empty_matches) == expected