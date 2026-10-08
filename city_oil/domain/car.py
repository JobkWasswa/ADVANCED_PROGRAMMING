"""Car is an Entity inside the JobCard aggregate.

Identity = plate number. Make, model or year may be corrected, but it is still
the same car.
"""
from .car_year import CarYear


class Car:
    def __init__(self, plate_number: str, make: str, model: str, year: CarYear):
        self._plate_number = plate_number
        self._make = make
        self._model = model
        self._year = year

    @property
    def plate_number(self) -> str:
        return self._plate_number

    @property
    def make(self) -> str:
        return self._make

    @property
    def model(self) -> str:
        return self._model

    @property
    def year(self) -> CarYear:
        return self._year

    def __eq__(self, other):
        return isinstance(other, Car) and self._plate_number == other._plate_number

    def __hash__(self):
        return hash(self._plate_number)
