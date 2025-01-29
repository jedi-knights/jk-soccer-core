from jk_soccer_core.models import Person


def test_default_person() -> None:
    # Arrange

    # Act
    person = Person()

    # Assert
    assert len(person.__dict__) == 1, (
        f"Expected 1 attribute, but got {len(person.__dict__)}"
    )
    assert person.name is None
