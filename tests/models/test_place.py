from jk_soccer_core.models import Place


def test_default_place() -> None:
    # Arrange

    # Act
    place = Place()

    # Assert
    assert place.name is None
