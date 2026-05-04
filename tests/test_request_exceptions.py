from __future__ import annotations

from unittest.mock import AsyncMock, Mock

import httpx
import pytest

from fakturoid_sdk.dispatcher import Dispatcher
from fakturoid_sdk.exceptions import ClientError, ServerError


@pytest.mark.parametrize(
    "status_code",
    [404, 400, 401, 402, 403, 415, 422, 429, 499],
)
async def test_client_error_exception(status_code: int) -> None:
    response = httpx.Response(
        status_code,
        headers={"Content-Type": "application/json"},
        content=b'{"error":""}',
    )

    client = Mock()
    client.request = AsyncMock(return_value=response)

    auth_provider = Mock()
    auth_provider.reauth = AsyncMock()
    credentials = Mock()
    credentials.get_access_token = Mock(return_value="test")
    auth_provider.get_credentials = Mock(return_value=credentials)

    dispatcher = Dispatcher(auth_provider, client, user_agent="Python SDK (test)")
    dispatcher.set_account_slug("account-slug")

    with pytest.raises(ClientError) as exc:
        await dispatcher.patch("/accounts/{accountSlug}/invoices/1.json", {"name": "Test"})

    assert exc.value.status_code == status_code


async def test_429_with_rate_limit_headers() -> None:
    response = httpx.Response(
        429,
        headers={
            "Content-Type": "application/json",
            "X-RateLimit-Policy": "default;q=400;w=60",
            "X-RateLimit": "default;r=0;t=45",
        },
        content=b'{"error":"Rate limit exceeded"}',
    )

    client = Mock()
    client.request = AsyncMock(return_value=response)

    auth_provider = Mock()
    auth_provider.reauth = AsyncMock()
    credentials = Mock()
    credentials.get_access_token = Mock(return_value="test")
    auth_provider.get_credentials = Mock(return_value=credentials)

    dispatcher = Dispatcher(auth_provider, client, user_agent="Python SDK (test)")
    dispatcher.set_account_slug("account-slug")

    with pytest.raises(ClientError) as exc:
        await dispatcher.patch("/accounts/{accountSlug}/invoices/1.json", {"name": "Test"})

    assert exc.value.status_code == 429
    assert exc.value.is_rate_limit_exceeded() is True

    resp = exc.value.response
    assert resp.get_rate_limit_quota() == 400
    assert resp.get_rate_limit_window() == 60
    assert resp.get_rate_limit_remaining() == 0
    assert resp.get_rate_limit_reset() == 45


async def test_400_is_not_rate_limit_exceeded() -> None:
    response = httpx.Response(
        400,
        headers={"Content-Type": "application/json"},
        content=b'{"error":""}',
    )

    client = Mock()
    client.request = AsyncMock(return_value=response)

    auth_provider = Mock()
    auth_provider.reauth = AsyncMock()
    credentials = Mock()
    credentials.get_access_token = Mock(return_value="test")
    auth_provider.get_credentials = Mock(return_value=credentials)

    dispatcher = Dispatcher(auth_provider, client, user_agent="Python SDK (test)")
    dispatcher.set_account_slug("account-slug")

    with pytest.raises(ClientError) as exc:
        await dispatcher.patch("/accounts/{accountSlug}/invoices/1.json", {"name": "Test"})

    assert exc.value.status_code == 400
    assert exc.value.is_rate_limit_exceeded() is False


@pytest.mark.parametrize("status_code", [503, 599])
async def test_server_error_exception(status_code: int) -> None:
    response = httpx.Response(
        status_code,
        headers={"Content-Type": "application/json"},
        content=b'{"error":""}',
    )

    client = Mock()
    client.request = AsyncMock(return_value=response)

    auth_provider = Mock()
    auth_provider.reauth = AsyncMock()
    credentials = Mock()
    credentials.get_access_token = Mock(return_value="test")
    auth_provider.get_credentials = Mock(return_value=credentials)

    dispatcher = Dispatcher(auth_provider, client, user_agent="Python SDK (test)")
    dispatcher.set_account_slug("account-slug")

    with pytest.raises(ServerError) as exc:
        await dispatcher.patch("/accounts/{accountSlug}/invoices/1.json", {"name": "Test"})

    assert exc.value.status_code == status_code
