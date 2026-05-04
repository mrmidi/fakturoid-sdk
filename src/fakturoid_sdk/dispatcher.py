from __future__ import annotations

import json
import logging
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlencode

import httpx
from tenacity import AsyncRetrying, retry_if_exception, stop_after_attempt, wait_random_exponential

from .auth import AuthProviderProtocol
from .exceptions import (
    AuthorizationFailedError,
    ClientError,
    ConnectionFailedError,
    FakturoidSdkError,
    RequestInfo,
    ServerError,
)
from .response import Response

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class RetryConfig:
    """Configuration for automatic request retries.

    Attributes:
        max_attempts: Maximum number of retry attempts.
        min_wait_seconds: Minimum wait time between retries.
        max_wait_seconds: Maximum wait time between retries.
        retry_on_rate_limit: Whether to retry when rate limited (429).
        retry_methods: HTTP methods that should be retried.
    """

    max_attempts: int = 3
    min_wait_seconds: float = 0.2
    max_wait_seconds: float = 2.0
    retry_on_rate_limit: bool = True
    retry_methods: frozenset[str] = frozenset({"GET"})


def _should_retry(exc: BaseException, *, retry_on_rate_limit: bool) -> bool:
    """Internal helper to determine if a request should be retried."""
    if isinstance(exc, ConnectionFailedError):
        return True
    if isinstance(exc, ServerError):
        return True
    if isinstance(exc, ClientError):
        return retry_on_rate_limit and exc.is_rate_limit_exceeded()
    return False


class Dispatcher:
    """Handles low-level HTTP request dispatching, authentication, and retries.

    Attributes:
        BASE_URL: The default base URL for Fakturoid API.
    """

    BASE_URL = "https://app.fakturoid.cz/api/v3"

    def __init__(
        self,
        authorization: AuthProviderProtocol,
        client: Any,
        account_slug: str | None = None,
        *,
        base_url: str = BASE_URL,
        retry: RetryConfig | None = None,
        user_agent: str,
    ) -> None:
        """Initializes the Dispatcher.

        See: https://www.fakturoid.cz/api/v3#user-agent

        Args:
            authorization: The authentication provider.
            client: The HTTPX async client.
            account_slug: The Fakturoid account slug.
            base_url: The base URL for the API.
            retry: Optional retry configuration.
            user_agent: The User-Agent string to identify the application.
        """
        self._authorization = authorization
        self._client = client
        self._account_slug = account_slug
        self._base_url = base_url
        self._retry = retry
        self._user_agent = user_agent

    def set_account_slug(self, account_slug: str) -> None:
        """Sets the account slug for subsequent requests.

        Args:
            account_slug: The Fakturoid account slug.
        """
        self._account_slug = account_slug

    async def get(self, path: str, query_params: Mapping[str, Any] | None = None) -> Response:
        """Performs a GET request.

        Args:
            path: The API endpoint path.
            query_params: Optional query parameters.

        Returns:
            The API response.
        """
        return await self._dispatch(path, method="GET", query_params=query_params)

    async def post(
        self,
        path: str,
        data: Mapping[str, Any] | None = None,
        query_params: Mapping[str, Any] | None = None,
    ) -> Response:
        """Performs a POST request.

        Args:
            path: The API endpoint path.
            data: Optional request body data.
            query_params: Optional query parameters.

        Returns:
            The API response.
        """
        return await self._dispatch(path, method="POST", data=data, query_params=query_params)

    async def patch(self, path: str, data: Mapping[str, Any]) -> Response:
        """Performs a PATCH request.

        Args:
            path: The API endpoint path.
            data: The request body data.

        Returns:
            The API response.
        """
        return await self._dispatch(path, method="PATCH", data=data)

    async def delete(self, path: str) -> Response:
        """Performs a DELETE request.

        Args:
            path: The API endpoint path.

        Returns:
            The API response.
        """
        return await self._dispatch(path, method="DELETE")

    async def _dispatch(
        self,
        path: str,
        *,
        method: str,
        query_params: Mapping[str, Any] | None = None,
        data: Mapping[str, Any] | None = None,
    ) -> Response:
        """Dispatches a request with optional retry logic."""
        retry_cfg = self._retry
        if retry_cfg is not None and method.upper() in retry_cfg.retry_methods:
            async for attempt in AsyncRetrying(
                stop=stop_after_attempt(retry_cfg.max_attempts),
                wait=wait_random_exponential(
                    multiplier=retry_cfg.min_wait_seconds,
                    max=retry_cfg.max_wait_seconds,
                ),
                retry=retry_if_exception(
                    lambda exc: _should_retry(
                        exc,
                        retry_on_rate_limit=retry_cfg.retry_on_rate_limit,
                    )
                ),
                reraise=True,
            ):
                with attempt:
                    if attempt.retry_state.attempt_number > 1:
                        logger.warning(
                            "Retrying %s %s (attempt %d)",
                            method,
                            path,
                            attempt.retry_state.attempt_number,
                        )
                    return await self._dispatch_once(
                        path,
                        method=method,
                        query_params=query_params,
                        data=data,
                    )

        return await self._dispatch_once(
            path,
            method=method,
            query_params=query_params,
            data=data,
        )

    async def _dispatch_once(
        self,
        path: str,
        *,
        method: str,
        query_params: Mapping[str, Any] | None = None,
        data: Mapping[str, Any] | None = None,
    ) -> Response:
        """Performs a single request dispatch."""
        if self._account_slug is None and "{accountSlug}" in path:
            raise FakturoidSdkError(
                "Account slug is not set. You must set it before calling this method."
            )

        await self._authorization.reauth()

        if self._authorization.get_credentials() is None:
            raise AuthorizationFailedError("Credentials are null")

        access_token = self._authorization.get_credentials().get_access_token()  # type: ignore[union-attr]

        body_bytes: bytes | None = None
        if data:
            body_bytes = json.dumps(data).encode("utf-8")

        url = f"{self._base_url}{path}".replace("{accountSlug}", self._account_slug or "")
        if query_params:
            url = f"{url}?{urlencode(query_params, doseq=True)}"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
            "User-Agent": self._user_agent,
        }

        request_info = RequestInfo(method=method, url=url, headers=headers, body=body_bytes)

        logger.debug("Dispatching request: %s %s", method, url)

        try:
            response = await self._client.request(method, url, headers=headers, content=body_bytes)
        except httpx.RequestError as exc:
            logger.error("Connection failed: %s %s - %s", method, url, exc)
            raise ConnectionFailedError(str(exc)) from exc

        wrapped = Response(response)
        status = wrapped.get_status_code()

        if 400 <= status < 600:
            logger.error("API error: %s %s - Status: %d", method, url, status)
            if 400 <= status < 500:
                raise ClientError(
                    response.reason_phrase or "",
                    status_code=status,
                    request=request_info,
                    response=wrapped,
                )
            raise ServerError(
                response.reason_phrase or "",
                status_code=status,
                request=request_info,
                response=wrapped,
            )

        return wrapped
