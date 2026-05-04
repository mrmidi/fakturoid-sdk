from __future__ import annotations

import datetime as dt
from collections.abc import Mapping
from decimal import Decimal, InvalidOperation
from enum import Enum
from typing import Any, TypeVar

TEnum = TypeVar("TEnum", bound=Enum)


def _get_int(data: Mapping[str, Any], key: str) -> int | None:
    """Extracts an integer from a dictionary."""
    value = data.get(key)
    return value if isinstance(value, int) else None


def _get_str(data: Mapping[str, Any], key: str) -> str | None:
    """Extracts a string from a dictionary."""
    value = data.get(key)
    return value if isinstance(value, str) else None


def _parse_date(value: str | None) -> dt.date | None:
    """Parses an ISO 8601 date string."""
    if value is None:
        return None
    try:
        return dt.date.fromisoformat(value)
    except ValueError:
        return None


def _parse_enum(enum_type: type[TEnum], value: str | None) -> TEnum | None:
    """Parses a string into an enum member."""
    if value is None:
        return None
    try:
        return enum_type(value)
    except ValueError:
        return None


def _get_decimal(data: Mapping[str, Any], key: str) -> Decimal | None:
    """Extracts a decimal from a dictionary."""
    value = data.get(key)
    if value is None:
        return None
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None


def _get_list(data: Mapping[str, Any], key: str) -> list[Any]:
    """Extracts a list from a dictionary."""
    value = data.get(key)
    return value if isinstance(value, list) else []
