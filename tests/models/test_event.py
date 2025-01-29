from jk_soccer_core.models import Event


def test_default_event() -> None:
    # Arrange

    # Act
    event = Event()

    # Assert
    assert len(event.__dict__) == 1, (
        f"Expected 1 attribute, but got {len(event.__dict__)}"
    )
    assert event.date is None
