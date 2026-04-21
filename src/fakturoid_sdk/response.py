from __future__ import annotations

import json
import re
from dataclasses import dataclass
from types import SimpleNamespace
from typing import Any

import httpx

from .exceptions import InvalidResponseError

JsonBody = dict[str, Any] | list[Any] | str | int | float | bool | None


def _to_namespace(value: JsonBody) -> Any:
    """Recursively converts a JSON body to a SimpleNamespace."""
    if isinstance(value, dict):
        return SimpleNamespace(**{k: _to_namespace(v) for k, v in value.items()})
    if isinstance(value, list):
        return [_to_namespace(v) for v in value]
    return value


@dataclass(frozen=True, slots=True)
class Response:
    """A wrapper around an HTTPX response.

    Attributes:
        original: The underlying HTTPX response.
    """

    original: httpx.Response

    def get_status_code(self) -> int:
        """Returns the HTTP status code."""
        return self.original.status_code

    def get_headers(self) -> dict[str, str]:
        """Returns all response headers."""
        return dict(self.original.headers)

    def get_header(self, name: str) -> str | None:
        """Returns the value of a specific response header.

        Args:
            name: The name of the header.

        Returns:
            The header value if found, None otherwise.
        """
        name_lower = name.lower()
        for header_name, header_value in self.original.headers.items():
            if header_name.lower() == name_lower:
                return header_value
        return None

    def get_bytes(self) -> bytes:
        """Returns the raw response content as bytes."""
        return self.original.content

    def get_body(self, *, return_json_as_dict: bool = False) -> Any:
        """Parses and returns the response body.

        If the response is JSON, it will be parsed. By default, JSON objects
        are converted to SimpleNamespace for dot-access.

        Args:
            return_json_as_dict: If True, returns JSON as plain dicts/lists.

        Returns:
            The parsed body (None if empty, parsed JSON, or raw text).

        Raises:
            InvalidResponseError: If the JSON body is malformed.
        """
        raw = self.original.content
        if raw == b"":
            return None

        if not self._is_json():
            return self.original.text

        try:
            parsed: JsonBody = json.loads(self.original.text)
        except json.JSONDecodeError as exc:
            raise InvalidResponseError("Invalid JSON response") from exc

        if return_json_as_dict:
            return parsed
        return _to_namespace(parsed)

    def _is_json(self) -> bool:
        """Checks if the response content type is JSON."""
        content_type = self.get_header("Content-Type")
        return content_type is not None and "application/json" in content_type

    def get_rate_limit_quota(self) -> int | None:
        """Returns the total rate limit quota."""
        policy = self.get_header("X-RateLimit-Policy")
        if policy is None:
            return None
        match = re.search(r"q=(\d+)", policy)
        return int(match.group(1)) if match else None

    def get_rate_limit_window(self) -> int | None:
        """Returns the rate limit window in seconds."""
        policy = self.get_header("X-RateLimit-Policy")
        if policy is None:
            return None
        match = re.search(r"w=(\d+)", policy)
        return int(match.group(1)) if match else None

    def get_rate_limit_remaining(self) -> int | None:
        """Returns the number of remaining requests in the current window."""
        rate_limit = self.get_header("X-RateLimit")
        if rate_limit is None:
            return None
        match = re.search(r"r=(\d+)", rate_limit)
        return int(match.group(1)) if match else None

    def get_rate_limit_reset(self) -> int | None:
        """Returns the time remaining until the rate limit resets (in seconds)."""
        rate_limit = self.get_header("X-RateLimit")
        if rate_limit is None:
            return None
        match = re.search(r"t=(\d+)", rate_limit)
        return int(match.group(1)) if match else None
