from jk_soccer_core.models import Place


def test_default_place() -> None:
    # Arrange

    # Act
    place = Place()

    # Assert
    assert len(place.__dict__) == 1, (
        f"Expected 1 attribute, but got {len(place.__dict__)}"
    )
    assert place.name is None
