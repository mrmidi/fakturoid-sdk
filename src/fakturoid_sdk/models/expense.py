from __future__ import annotations

import datetime as dt
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from fakturoid_sdk.enums import ExpenseStatus

from .base import _get_int, _get_str, _parse_date, _parse_enum


@dataclass(frozen=True, slots=True)
class Expense:
    """Typed view over an expense JSON object.

    This model is intentionally tolerant: the API response may contain fields we
    do not model yet; they remain accessible via `raw`.

    Attributes:
        raw: The raw JSON data from the API response.
    """

    raw: Mapping[str, Any]

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Expense:
        """Creates an Expense instance from a dictionary.

        Args:
            data: The dictionary containing expense data.

        Returns:
            A new Expense instance.
        """
        return cls(raw=data)

    @property
    def id(self) -> int | None:
        """The unique identifier of the expense."""
        return _get_int(self.raw, "id")

    @property
    def number(self) -> str | None:
        """The expense number."""
        return _get_str(self.raw, "number")

    @property
    def status(self) -> ExpenseStatus | None:
        """The current status of the expense."""
        return _parse_enum(ExpenseStatus, _get_str(self.raw, "status"))

    @property
    def subject_id(self) -> int | None:
        """The identifier of the subject (vendor) associated with the expense."""
        return _get_int(self.raw, "subject_id")

    @property
    def paid_on(self) -> dt.date | None:
        """The date when the expense was paid."""
        return _parse_date(_get_str(self.raw, "paid_on"))
