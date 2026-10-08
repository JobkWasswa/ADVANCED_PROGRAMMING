"""Domain events: immutable records of something that happened (past tense)."""
from dataclasses import dataclass


@dataclass(frozen=True)
class JobCompleted:
    """BR5 trigger. Raised by JobCard when it moves to COMPLETED.

    part_lines is a tuple of (part_id, quantity) pairs that the job used.
    """
    job_id: str
    part_lines: tuple[tuple[str, int], ...]
