"""BR1 - Value rule: a car's year must be between 1980 and 2027.

CarYear is a Value Object: it has no identity of its own. Two CarYear(2012)
objects are interchangeable, it is immutable (frozen), and it validates itself
on creation so an invalid year can never exist anywhere in the system.
"""
from dataclasses import dataclass

from .errors import InvalidYearError

MIN_YEAR = 1980
MAX_YEAR = 2027


@dataclass(frozen=True)
class CarYear:
    value: int

    def __post_init__(self):
        if isinstance(self.value, bool) or not isinstance(self.value, int):
            raise InvalidYearError("Year must be a whole number")
        if not MIN_YEAR <= self.value <= MAX_YEAR:
            raise InvalidYearError(
                f"Year {self.value} is outside the allowed range {MIN_YEAR}-{MAX_YEAR}"
            )
