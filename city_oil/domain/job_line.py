"""A line on a job card: either a part (part_id set) or labour (part_id None).

Child entity of the JobCard aggregate. It is only reachable through JobCard.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class JobLine:
    line_id: int
    description: str
    quantity: int          # number of parts, or hours of labour
    unit_price: int        # price per part, or hourly rate
    part_id: Optional[str] = None

    @property
    def line_total(self) -> int:
        return self.quantity * self.unit_price
