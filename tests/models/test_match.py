import pytest

from jk_soccer_core.models import Match, Team


@pytest.fixture
def team_a():
    return Team(name="Team A")


@pytest.fixture
def team_b():
    return Team(name="Team B")


@pytest.fixture
def match(team_a, team_b):
    return Match(home=team_a, away=team_b, home_score=2, away_score=1)


def test_default_match() -> None:
    # Arrange

    # Act
    match = Match()

    # Assert
    assert len(match.__dict__) == 5, (
        f"Expected 5 attributes, but got {len(match.__dict__)}"
    )
    assert match.date is None, f"Expected None, but got {match.date}"
    assert match.home is None, f"Expected None, but got {match.home_team}"
    assert match.away is None, f"Expected None, but got {match.away_team}"
    assert match.home_score == 0, f"Expected 0, but got {match.home_score}"
    assert match.away_score == 0, f"Expected 0, but got {match.away_score}"


def test_contains_team_home_team(match, team_a):
    assert match.contains_team(team_a.name) is True, f"Expected True, but got {match.contains_team(team_a.name)}"


def test_contains_team_away_team(match, team_b):
    assert match.contains_team(team_b.name) is True, f"Expected True, but got {match.contains_team(team_b.name)}"


def test_contains_team_not_in_match(match):
    assert match.contains_team("Team C") is False, f"Expected False, but got {match.contains_team('Team C')}"


def test_contains_team_empty_string(match):
    assert match.contains_team("") is False, f"Expected False, but got {match.contains_team('')}"


def test_contains_team_none(match):
    assert match.contains_team(None) is False, f"Expected False, but got {match.contains_team(None)}"


def test_winner_home_team_wins(match, team_a):
    assert match.winner() == team_a, f"Expected {team_a}, but got {match.winner()}"


def test_winner_away_team_wins(team_a, team_b):
    match = Match(home=team_a, away=team_b, home_score=1, away_score=2)
    assert match.winner() == team_b, f"Expected {team_b}, but got {match.winner()}"


def test_winner_draw(team_a, team_b):
    match = Match(home=team_a, away=team_b, home_score=1, away_score=1)
    assert match.winner() is None, f"Expected None, but got {match.winner()}"


def test_winner_no_scores(team_a, team_b):
    match = Match(home=team_a, away=team_b, home_score=0, away_score=0)
    assert match.winner() is None, f"Expected None, but got {match.winner()}"


def test_winner_no_teams():
    match = Match(home=None, away=None, home_score=1, away_score=1)
    assert match.winner() is None, f"Expected None, but got {match.winner()}"


def test_loser_home_team_loses(team_a, team_b):
    match = Match(home=team_a, away=team_b, home_score=1, away_score=2)
    assert match.loser() == team_a, f"Expected {team_a}, but got {match.loser()}"


def test_loser_away_team_loses(match, team_b):
    assert match.loser() == team_b, f"Expected {team_b}, but got {match.loser()}"


def test_loser_draw(team_a, team_b):
    match = Match(home=team_a, away=team_b, home_score=1, away_score=1)
    assert match.loser() is None, f"Expected None, but got {match.loser()}"


def test_loser_no_scores(team_a, team_b):
    match = Match(home=team_a, away=team_b, home_score=0, away_score=0)
    assert match.loser() is None, f"Expected None, but got {match.loser()}"


def test_loser_no_teams():
    match = Match(home=None, away=None, home_score=1, away_score=1)
    assert match.loser() is None, f"Expected None, but got {match.loser()}"

def test_is_draw_true(team_a, team_b):
    match = Match(home=team_a, away=team_b, home_score=1, away_score=1)
    assert match.is_draw() is True, f"Expected True, but got {match.is_draw()}"

def test_is_draw_false(match):
    assert match.is_draw() is False, f"Expected False, but got {match.is_draw()}"

def test_is_draw_no_scores(team_a, team_b):
    match = Match(home=team_a, away=team_b, home_score=0, away_score=0)
    assert match.is_draw() is True, f"Expected True, but got {match.is_draw()}"

def test_is_draw_no_teams():
    match = Match(home=None, away=None, home_score=1, away_score=1)
    assert match.is_draw() is True, f"Expected True, but got {match.is_draw()}"

def test_is_draw_none_scores(team_a, team_b):
    match = Match(home=team_a, away=team_b, home_score=None, away_score=None)
    assert match.is_draw() is True, f"Expected True, but got {match.is_draw()}"
