from __future__ import annotations

import datetime as dt
from collections.abc import Mapping
from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from fakturoid_sdk.enums import InvoiceStatus

from .base import _get_decimal, _get_int, _get_list, _get_str, _parse_date, _parse_enum


@dataclass(frozen=True, slots=True)
class Invoice:
    """Typed view over an invoice JSON object.

    This model is intentionally tolerant: the API response may contain fields we
    do not model yet; they remain accessible via `raw`.

    Attributes:
        raw: The raw JSON data from the API response.
    """

    raw: Mapping[str, Any]

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Invoice:
        """Creates an Invoice instance from a dictionary.

        Args:
            data: The dictionary containing invoice data.

        Returns:
            A new Invoice instance.
        """
        return cls(raw=data)

    @property
    def id(self) -> int | None:
        """The unique identifier of the invoice."""
        return _get_int(self.raw, "id")

    @property
    def number(self) -> str | None:
        """The invoice number (e.g., '2023-0001')."""
        return _get_str(self.raw, "number")

    @property
    def custom_id(self) -> str | None:
        """The custom identifier of the invoice."""
        return _get_str(self.raw, "custom_id")

    @property
    def status(self) -> InvoiceStatus | None:
        """The current status of the invoice."""
        return _parse_enum(InvoiceStatus, _get_str(self.raw, "status"))

    @property
    def subject_id(self) -> int | None:
        """The identifier of the subject (customer) associated with the invoice."""
        return _get_int(self.raw, "subject_id")

    @property
    def correction_id(self) -> int | None:
        """Identifier of the invoice/correction linked by Fakturoid."""
        return _get_int(self.raw, "correction_id")

    @property
    def related_id(self) -> int | None:
        """The identifier of the related document."""
        return _get_int(self.raw, "related_id")

    @property
    def due_on(self) -> dt.date | None:
        """The date when the invoice is due."""
        return _parse_date(_get_str(self.raw, "due_on"))

    @property
    def issued_on(self) -> dt.date | None:
        """The date when the invoice was issued."""
        return _parse_date(_get_str(self.raw, "issued_on"))

    @property
    def document_type(self) -> str | None:
        """The type of the document (e.g., 'invoice', 'proforma')."""
        return _get_str(self.raw, "document_type")

    @property
    def currency(self) -> str | None:
        """The currency of the invoice (e.g., 'CZK', 'EUR')."""
        return _get_str(self.raw, "currency")

    @property
    def subtotal(self) -> Decimal | None:
        """The subtotal amount of the invoice."""
        return _get_decimal(self.raw, "subtotal")

    @property
    def total(self) -> Decimal | None:
        """The total amount of the invoice."""
        return _get_decimal(self.raw, "total")

    @property
    def remaining_amount(self) -> Decimal | None:
        """The remaining amount to be paid on the invoice."""
        return _get_decimal(self.raw, "remaining_amount")

    @property
    def remaining_native_amount(self) -> Decimal | None:
        """The remaining amount to be paid in the account's native currency."""
        return _get_decimal(self.raw, "remaining_native_amount")

    @property
    def native_subtotal(self) -> Decimal | None:
        """The subtotal amount in the account's native currency."""
        return _get_decimal(self.raw, "native_subtotal")

    @property
    def native_total(self) -> Decimal | None:
        """The total amount in the account's native currency."""
        return _get_decimal(self.raw, "native_total")

    @property
    def lines(self) -> list[Any]:
        """The line items of the invoice."""
        return _get_list(self.raw, "lines")

    @property
    def payments(self) -> list[Any]:
        """The payments associated with the invoice."""
        return _get_list(self.raw, "payments")

    @property
    def attachments(self) -> list[Any]:
        """The attachments associated with the invoice."""
        return _get_list(self.raw, "attachments")

    @property
    def html_url(self) -> str | None:
        """The HTML URL of the invoice."""
        return _get_str(self.raw, "html_url")

    @property
    def public_html_url(self) -> str | None:
        """The public HTML URL of the invoice."""
        return _get_str(self.raw, "public_html_url")

    @property
    def url(self) -> str | None:
        """The API URL of the invoice."""
        return _get_str(self.raw, "url")

    @property
    def pdf_url(self) -> str | None:
        """The PDF URL of the invoice."""
        return _get_str(self.raw, "pdf_url")
