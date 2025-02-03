import pytest
from jk_soccer_core.models import Match, Team
from jk_soccer_core.calculations.meetings import MeetingsCalculation


@pytest.fixture
def teams():
    return Team(name="Team A"), Team(name="Team B"), Team(name="Team C")


def test_no_matches(teams):
    team1, team2, _ = teams
    assert (
        MeetingsCalculation(team_name1=team1.name, team_name2=team2.name).calculate([])
        == 0
    )


def test_no_meetings(teams):
    team1, team2, team3 = teams
    matches = [
        Match(home=team1, away=team3, home_score=1, away_score=0),
        Match(home=team2, away=team3, home_score=2, away_score=2),
    ]
    assert (
        MeetingsCalculation(team_name1=team1.name, team_name2=team2.name).calculate(
            matches
        )
        == 0
    )


def test_single_meeting(teams):
    team1, team2, _ = teams
    matches = [Match(home=team1, away=team2, home_score=1, away_score=0)]
    assert (
        MeetingsCalculation(team_name1=team1.name, team_name2=team2.name).calculate(
            matches
        )
        == 1
    )


def test_multiple_meetings(teams):
    team1, team2, team3 = teams
    matches = [
        Match(home=team1, away=team2, home_score=1, away_score=0),
        Match(home=team2, away=team1, home_score=2, away_score=1),
        Match(home=team1, away=team3, home_score=0, away_score=0),
    ]
    assert (
        MeetingsCalculation(team_name1=team1.name, team_name2=team2.name).calculate(
            matches
        )
        == 2
    )


def test_empty_team_names(teams):
    team1, team2, _ = teams
    matches = [Match(home=team1, away=team2, home_score=1, away_score=0)]
    assert (
        MeetingsCalculation(team_name1=None, team_name2=team2.name).calculate(matches)
        == 0
    )
    assert (
        MeetingsCalculation(team_name1=team1.name, team_name2=None).calculate(matches)
        == 0
    )
    assert MeetingsCalculation(team_name1=None, team_name2=None).calculate(matches) == 0


def test_same_team_names(teams):
    team1, _, _ = teams
    matches = [Match(home=team1, away=team1, home_score=1, away_score=0)]
    assert (
        MeetingsCalculation(team_name1=team1.name, team_name2=team1.name).calculate(
            matches
        )
        == 1
    )
