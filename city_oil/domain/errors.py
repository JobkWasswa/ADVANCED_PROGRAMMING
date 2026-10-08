"""Domain errors. Each business rule fails with its own named error."""


class DomainError(Exception):
    """Base class for every business-rule violation."""


class InvalidYearError(DomainError):          # BR1
    pass


class InvalidJobStateError(DomainError):      # illegal state transition (general)
    pass


class JobNotApprovedError(DomainError):       # BR2
    pass


class JobLockedError(DomainError):            # BR3
    pass


class PartDoesNotFitError(DomainError):       # BR4
    pass


class InsufficientStockError(DomainError):    # BR5 (raised by Part, Aggregate B)
    pass


class InvalidQuantityError(DomainError):
    pass
