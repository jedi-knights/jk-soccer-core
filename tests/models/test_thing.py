from jk_soccer_core.models import Thing


def test_default_thing() -> None:
    # Arrange

    # Act
    thing = Thing()

    # Assert
    assert len(thing.__dict__) == 2, (
        f"Expected 1 attribute, but got {len(thing.__dict__)}"
    )
    assert thing.name is None
    assert thing.description is None


def test_valid_thing() -> None:
    # Arrange

    # Act
    thing = Thing(name="foo", description="bar")

    # Assert
    assert thing.name == "foo"
    assert thing.description == "bar"
