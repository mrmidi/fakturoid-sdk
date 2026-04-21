from __future__ import annotations

import datetime as dt
from typing import Any, TypeAlias

"""Common type definitions for the Fakturoid SDK."""

JsonValue: TypeAlias = dict[str, Any] | list[Any] | str | int | float | bool | None
"""Type alias for a JSON-serializable value."""

# Convenience input types for pythonic client resources.
DateLike: TypeAlias = str | dt.date | dt.datetime
"""Type alias for values that can be coerced to an ISO 8601 date string."""
