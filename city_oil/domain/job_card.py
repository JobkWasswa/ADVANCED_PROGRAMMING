"""JobCard - Aggregate Root A.

Rules enforced here:
  BR2 (identity/state): a job can only be completed after it was approved.
  BR3 (invariant):      once approved, the part and labour lines cannot change.
                        approve() records the total as the approved estimate, and
                        because the lines are locked from then on, the total can
                        never go above that estimate.
  BR5 (trigger):        completing the job raises the JobCompleted event.
                        JobCard does NOT touch Part; it only announces the fact.
"""
from enum import Enum
from typing import List, Optional

from .car import Car
from .errors import (
    InvalidJobStateError,
    InvalidQuantityError,
    JobLockedError,
    JobNotApprovedError,
)
from .events import JobCompleted
from .job_line import JobLine


class JobStatus(Enum):
    OPEN = "OPEN"
    DIAGNOSED = "DIAGNOSED"
    APPROVED = "APPROVED"
    COMPLETED = "COMPLETED"


class JobCard:
    def __init__(self, job_id: str, car: Car):
        self._job_id = job_id
        self._car = car
        self._status = JobStatus.OPEN
        self._diagnosis = ""
        self._lines: List[JobLine] = []
        self._approved_estimate: Optional[int] = None
        self._next_line_id = 1
        self._events: list = []

    # ---- read-only access -------------------------------------------------
    @property
    def job_id(self) -> str:
        return self._job_id

    @property
    def car(self) -> Car:
        return self._car

    @property
    def status(self) -> JobStatus:
        return self._status

    @property
    def lines(self) -> tuple:
        return tuple(self._lines)

    @property
    def approved_estimate(self) -> Optional[int]:
        return self._approved_estimate

    def total(self) -> int:
        return sum(line.line_total for line in self._lines)

    # ---- behaviour --------------------------------------------------------
    def diagnose(self, notes: str) -> None:
        if self._status is not JobStatus.OPEN:
            raise InvalidJobStateError("Only an open job card can be diagnosed")
        self._diagnosis = notes
        self._status = JobStatus.DIAGNOSED

    def add_part_line(self, part_id: str, description: str, quantity: int, unit_price: int) -> None:
        self._ensure_lines_can_change()           # BR3
        self._ensure_positive(quantity)
        self._append_line(description, quantity, unit_price, part_id)

    def add_labour_line(self, description: str, hours: int, hourly_rate: int) -> None:
        self._ensure_lines_can_change()           # BR3
        self._ensure_positive(hours)
        self._append_line(description, hours, hourly_rate, None)

    def approve(self) -> None:
        if self._status is not JobStatus.DIAGNOSED:
            raise InvalidJobStateError("Only a diagnosed job card can be approved")
        if not self._lines:
            raise InvalidJobStateError("Cannot approve a job card with no lines")
        self._approved_estimate = self.total()
        self._status = JobStatus.APPROVED

    def complete(self) -> None:
        if self._status is not JobStatus.APPROVED:          # BR2
            raise JobNotApprovedError("A job can only be completed after it is approved")
        self._status = JobStatus.COMPLETED
        part_lines = tuple(
            (line.part_id, line.quantity) for line in self._lines if line.part_id is not None
        )
        self._events.append(JobCompleted(self._job_id, part_lines))   # BR5 trigger

    def pull_events(self) -> list:
        """Hand over the recorded events and clear them."""
        events, self._events = self._events, []
        return events

    # ---- private helpers --------------------------------------------------
    def _ensure_lines_can_change(self) -> None:
        if self._status in (JobStatus.APPROVED, JobStatus.COMPLETED):
            raise JobLockedError("Lines cannot be changed after the job card is approved")

    @staticmethod
    def _ensure_positive(quantity: int) -> None:
        if quantity <= 0:
            raise InvalidQuantityError("Quantity must be greater than zero")

    def _append_line(self, description, quantity, unit_price, part_id) -> None:
        self._lines.append(JobLine(self._next_line_id, description, quantity, unit_price, part_id))
        self._next_line_id += 1
