from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .response import Response


class FakturoidSdkError(Exception):
    """Base error class for all Fakturoid SDK errors."""


class InvalidResponseError(FakturoidSdkError):
    """Raised when an HTTP response cannot be parsed (e.g., invalid JSON)."""


class InvalidDataError(FakturoidSdkError):
    """Raised when provided data is malformed or missing required fields."""


class AuthorizationFailedError(FakturoidSdkError):
    """Raised when authentication fails or credentials are invalid."""


class ConnectionFailedError(FakturoidSdkError):
    """Raised when a network-level error occurs while sending a request."""


@dataclass(frozen=True, slots=True)
class RequestInfo:
    """Information about an HTTP request.

    Attributes:
        method: HTTP method (e.g., 'GET', 'POST').
        url: Full request URL.
        headers: Request headers.
        body: Raw request body.
    """

    method: str
    url: str
    headers: Mapping[str, str]
    body: bytes | None = None


class RequestError(FakturoidSdkError):
    """Error raised when an API request fails (4xx or 5xx status code).

    Attributes:
        status_code: The HTTP status code.
        request: The request information.
        response: The wrapped response.
    """

    def __init__(
        self,
        message: str,
        *,
        status_code: int,
        request: RequestInfo,
        response: Response,
        cause: Exception | None = None,
    ) -> None:
        """Initializes the RequestError.

        Args:
            message: The error message.
            status_code: The HTTP status code.
            request: The RequestInfo object.
            response: The Response object.
            cause: The underlying exception, if any.
        """
        self.status_code = status_code
        self.request = request
        self.response = response
        self.__cause__ = cause

        error_details = self._get_error_details()
        if error_details:
            message = f"{message}: {error_details}"

        super().__init__(message)

    def _get_error_details(self) -> str | None:
        """Attempts to extract error details from the response body."""
        try:
            body = self.response.get_body(return_json_as_dict=True)
            if not isinstance(body, dict):
                return str(body) if body else None

            # Handle {"errors": {"field": ["msg"]}}
            if "errors" in body:
                return str(body["errors"])

            # Handle {"error": "code", "error_description": "msg"}
            error_code = body.get("error")
            error_desc = body.get("error_description")

            if error_code and error_desc:
                return f"{str(error_code)}: {str(error_desc)}"
            if error_desc:
                return str(error_desc)
            if error_code:
                return str(error_code)

            return str(body)
        except Exception:
            pass
        return None


class ClientError(RequestError):
    """Error raised for 4xx client-side errors."""

    def is_rate_limit_exceeded(self) -> bool:
        """Checks if the error is due to a rate limit (429)."""
        return self.status_code == 429


class ServerError(RequestError):
    """Error raised for 5xx server-side errors."""

    pass
