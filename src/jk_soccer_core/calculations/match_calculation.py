from collections.abc import Iterable
from typing import Protocol, TypeVar

from jk_soccer_core.models import Match


T_co = TypeVar("T_co", covariant=True)


class MatchCalculation(Protocol[T_co]):
    """Structural interface for objects that compute a value from a sequence of matches."""

    def calculate(self, matches: Iterable[Match]) -> T_co: ...
