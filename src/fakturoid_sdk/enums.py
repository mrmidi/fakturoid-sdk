from __future__ import annotations

from enum import Enum


class _StrEnum(str, Enum):
    """A Python 3.10-compatible string enum.

    We avoid `enum.StrEnum` since the SDK targets Python 3.10.
    """

    def __str__(self) -> str:  # pragma: no cover
        return str(self.value)


class InvoiceStatus(_StrEnum):
    """Possible statuses of an invoice."""

    OPEN = "open"
    SENT = "sent"
    OVERDUE = "overdue"
    PAID = "paid"
    CANCELLED = "cancelled"


class ExpenseStatus(_StrEnum):
    """Possible statuses of an expense."""

    OPEN = "open"
    OVERDUE = "overdue"
    PAID = "paid"


class InvoiceEvent(_StrEnum):
    """Actions that can be performed on an invoice."""

    MARK_AS_SENT = "mark_as_sent"
    CANCEL = "cancel"
    UNDO_CANCEL = "undo_cancel"
    PAY = "pay"


class ExpenseEvent(_StrEnum):
    """Actions that can be performed on an expense."""

    REMOVE_PAYMENT = "remove_payment"
    DELIVER = "deliver"
    PAY = "pay"
    LOCK = "lock"
    UNLOCK = "unlock"
