from __future__ import annotations

import warnings
from typing import Any


class Provider:
    """Base class for all raw API providers."""

    def filter_options(
        self,
        options: dict[str, Any] | None,
        allowed_keys: list[str] | None = None,
    ) -> dict[str, Any]:
        """Filters a dictionary of options, keeping only allowed keys.

        If unknown keys are found, a UserWarning is issued.

        Args:
            options: The dictionary of options to filter.
            allowed_keys: A list of keys that are allowed.

        Returns:
            A new dictionary containing only the allowed options.
        """
        if not options:
            return {}

        allowed = {key.lower() for key in (allowed_keys or [])}
        normalized = {k.lower(): v for k, v in options.items()}

        result: dict[str, Any] = {}
        unknown: list[str] = []

        for key, value in normalized.items():
            if key not in allowed:
                unknown.append(key)
            else:
                result[key] = value

        if unknown:
            warnings.warn(
                f"Unknown option keys: {', '.join(unknown)}",
                category=UserWarning,
                stacklevel=2,
            )

        return result
