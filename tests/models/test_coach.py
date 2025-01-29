from jk_soccer_core.models import Coach


def test_default_coach() -> None:
    # Arrange

    # Act
    coach = Coach()

    # Assert
    assert len(coach.__dict__) == 2, (
        f"Expected 2 attributes, but got {len(coach.__dict__)}"
    )
    assert coach.name is None
