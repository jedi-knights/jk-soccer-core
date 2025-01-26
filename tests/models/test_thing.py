import pytest

from pydantic import ValidationError

from jk_soccer_core.models import Thing


def test_valid_thing() -> None:
    # Arrange

    # Act
    thing = Thing(name='foo', description='bar')

    # Assert
    assert thing.name == 'foo'
    assert thing.description == 'bar'
