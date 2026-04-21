from __future__ import annotations

import datetime as dt
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from fakturoid_sdk.enums import InvoiceStatus

from .base import _get_int, _get_str, _parse_date, _parse_enum


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
    def status(self) -> InvoiceStatus | None:
        """The current status of the invoice."""
        return _parse_enum(InvoiceStatus, _get_str(self.raw, "status"))

    @property
    def subject_id(self) -> int | None:
        """The identifier of the subject (customer) associated with the invoice."""
        return _get_int(self.raw, "subject_id")

    @property
    def due_on(self) -> dt.date | None:
        """The date when the invoice is due."""
        return _parse_date(_get_str(self.raw, "due_on"))
