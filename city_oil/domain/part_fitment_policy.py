"""BR4 - Cross-concept rule: a part must fit the car.

This is a Domain Service. The decision needs facts from two different
concepts (Part: compatible makes and years; Car: make and year), and it does
not belong naturally on either one. The service is stateless.
"""
from .car import Car
from .errors import PartDoesNotFitError
from .part import Part


class PartFitmentPolicy:
    def ensure_fits(self, part: Part, car: Car) -> None:
        if car.make.lower() not in part.compatible_makes:
            raise PartDoesNotFitError(
                f"Part {part.part_id} does not fit make '{car.make}'"
            )
        if not part.year_from <= car.year.value <= part.year_to:
            raise PartDoesNotFitError(
                f"Part {part.part_id} fits years {part.year_from}-{part.year_to}, "
                f"not {car.year.value}"
            )
