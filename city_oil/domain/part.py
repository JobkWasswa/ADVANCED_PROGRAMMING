"""Part - Aggregate Root B.

Invariant: stock_qty never goes below zero.
BR5 (receiver): Part decides whether it can give up the requested stock. If
there is not enough, Part itself rejects the follow-up action.
"""
from collections.abc import Iterable

from .errors import InsufficientStockError, InvalidQuantityError


class Part:
    def __init__(self, part_id: str, name: str, stock_qty: int, unit_price: int,
                 compatible_makes: Iterable[str], year_from: int, year_to: int):
        if stock_qty < 0:
            raise InvalidQuantityError("Stock cannot be negative")
        self._part_id = part_id
        self._name = name
        self._stock_qty = stock_qty
        self._unit_price = unit_price
        self._compatible_makes = frozenset(make.lower() for make in compatible_makes)
        self._year_from = year_from
        self._year_to = year_to

    @property
    def part_id(self) -> str:
        return self._part_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def stock_qty(self) -> int:
        return self._stock_qty

    @property
    def unit_price(self) -> int:
        return self._unit_price

    @property
    def compatible_makes(self) -> frozenset:
        return self._compatible_makes

    @property
    def year_from(self) -> int:
        return self._year_from

    @property
    def year_to(self) -> int:
        return self._year_to

    def can_supply(self, quantity: int) -> bool:
        return 0 < quantity <= self._stock_qty

    def ensure_can_supply(self, quantity: int) -> None:
        if quantity <= 0:
            raise InvalidQuantityError("Quantity must be greater than zero")
        if quantity > self._stock_qty:
            raise InsufficientStockError(
                f"Not enough stock for part {self._part_id}: need {quantity}, have {self._stock_qty}"
            )

    def reduce_stock(self, quantity: int) -> None:
        self.ensure_can_supply(quantity)
        self._stock_qty -= quantity
