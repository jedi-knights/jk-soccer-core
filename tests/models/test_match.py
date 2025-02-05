import pytest

from jk_soccer_core.models import Match, is_draw, winner, loser


@pytest.mark.parametrize(
    "home_team, away_team, home_score, away_score, expected",
    [
        ("Team A", "Team B", 1, 1, True),  # Draw
        ("Team A", "Team B", 2, 1, False),  # Not a draw
        ("Team A", "Team B", 0, 0, True),  # Draw
        ("Team A", "Team B", 3, 2, False),  # Not a draw
        ("Team A", "Team B", -1, -1, True),  # Draw with negative scores
        ("Team A", "Team B", 100, 100, True),  # Draw with high scores
        ("Team A", "Team B", 0, 1, False),  # Not a draw with one team having zero score
        ("Team A", "Team B", 1, 0, False),  # Not a draw with one team having zero score
    ],
)
def test_is_draw(home_team, away_team, home_score, away_score, expected):
    match = Match(home_team, away_team, home_score, away_score)
    assert is_draw(match) == expected


@pytest.mark.parametrize(
    "home_team, away_team, home_score, away_score, expected",
    [
        ("Team A", "Team B", 1, 1, None),  # Draw
        ("Team A", "Team B", 2, 1, "Team A"),  # Home team wins
        ("Team A", "Team B", 0, 0, None),  # Draw
        ("Team A", "Team B", 2, 3, "Team B"),  # Away team wins
        ("Team A", "Team B", -1, -1, None),  # Draw with negative scores
        ("Team A", "Team B", 100, 99, "Team A"),  # Home team wins with high scores
        (
            "Team A",
            "Team B",
            0,
            1,
            "Team B",
        ),  # Away team wins with one team having zero score
        (
            "Team A",
            "Team B",
            1,
            0,
            "Team A",
        ),  # Home team wins with one team having zero score
    ],
)
def test_winner(home_team, away_team, home_score, away_score, expected):
    match = Match(home_team, away_team, home_score, away_score)
    assert winner(match) == expected


@pytest.mark.parametrize(
    "home_team, away_team, home_score, away_score, expected",
    [
        ("Team Z", "Team B", 1, 1, None),  # Draw
        ("Team Z", "Team B", 2, 1, "Team B"),  # Home team wins
        ("Team Z", "Team B", 0, 0, None),  # Draw
        ("Team Z", "Team B", 2, 3, "Team Z"),  # Away team wins
        ("Team Z", "Team B", -1, -1, None),  # Draw with negative scores
        ("Team Z", "Team B", 100, 99, "Team B"),  # Home team wins with high scores
        (
            "Team Z",
            "Team B",
            0,
            1,
            "Team Z",
        ),  # Away team wins with one team having zero score
        (
            "Team Z",
            "Team B",
            1,
            0,
            "Team B",
        ),  # Home team wins with one team having zero score
    ],
)
def test_loser(home_team, away_team, home_score, away_score, expected):
    match = Match(home_team, away_team, home_score, away_score)
    assert loser(match) == expected
