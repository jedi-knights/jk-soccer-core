from jk_soccer_core.models import Match


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
