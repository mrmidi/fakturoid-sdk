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
    """Actions that can be performed on an invoice.

    See: https://www.fakturoid.cz/api/v3/invoices#invoice-actions
    """

    MARK_AS_SENT = "mark_as_sent"
    CANCEL = "cancel"
    UNDO_CANCEL = "undo_cancel"
    LOCK = "lock"
    UNLOCK = "unlock"
    MARK_AS_UNCOLLECTIBLE = "mark_as_uncollectible"
    UNDO_UNCOLLECTIBLE = "undo_uncollectible"
    PAY = "pay"  # Deprecated; use Invoices.create_payment()


class ExpenseEvent(_StrEnum):
    """Actions that can be performed on an expense.

    See: https://www.fakturoid.cz/api/v3/expenses#post-accounts-slug-expenses-id-fire-json
    """

    LOCK = "lock"
    UNLOCK = "unlock"
