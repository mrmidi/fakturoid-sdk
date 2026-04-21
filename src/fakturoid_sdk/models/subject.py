from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from .base import _get_int, _get_str


@dataclass(frozen=True, slots=True)
class Subject:
    """Typed view over a subject/contact JSON object.

    This model is intentionally tolerant: the API response may contain fields we
    do not model yet; they remain accessible via `raw`.

    Attributes:
        raw: The raw JSON data from the API response.
    """

    raw: Mapping[str, Any]

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Subject:
        """Creates a Subject instance from a dictionary.

        Args:
            data: The dictionary containing subject data.

        Returns:
            A new Subject instance.
        """
        return cls(raw=data)

    @property
    def id(self) -> int | None:
        """The unique identifier of the subject."""
        return _get_int(self.raw, "id")

    @property
    def name(self) -> str | None:
        """The name of the subject (company name or person name)."""
        return _get_str(self.raw, "name")
