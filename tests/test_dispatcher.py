from unittest.mock import AsyncMock, Mock

import httpx
import pytest

from fakturoid_sdk.dispatcher import Dispatcher
from fakturoid_sdk.exceptions import FakturoidSdkError


async def test_required_account_slug_missing() -> None:
    client = Mock()
    client.request = AsyncMock()

    auth_provider = Mock()
    auth_provider.reauth = AsyncMock()
    auth_provider.get_credentials = Mock()

    dispatcher = Dispatcher(auth_provider, client)

    with pytest.raises(
        FakturoidSdkError,
        match=r"Account slug is not set\. You must set it before calling this method\.",
    ):
        await dispatcher.patch("/accounts/{accountSlug}/invoices/1.json", {"name": "Test"})

    client.request.assert_not_awaited()
    auth_provider.reauth.assert_not_awaited()
    auth_provider.get_credentials.assert_not_called()


async def test_required_account_slug_present() -> None:
    client = Mock()
    client.request = AsyncMock(return_value=httpx.Response(200, content=b""))

    auth_provider = Mock()
    auth_provider.reauth = AsyncMock()

    credentials = Mock()
    credentials.get_access_token = Mock(return_value="test")
    auth_provider.get_credentials = Mock(return_value=credentials)

    dispatcher = Dispatcher(auth_provider, client, "test")
    await dispatcher.patch("/accounts/{accountSlug}/invoices/1.json", {"name": "Test"})

    assert client.request.await_count == 1


async def test_not_required_account_slug_missing() -> None:
    client = Mock()
    client.request = AsyncMock(return_value=httpx.Response(200, content=b""))

    auth_provider = Mock()
    auth_provider.reauth = AsyncMock()

    credentials = Mock()
    credentials.get_access_token = Mock(return_value="test")
    auth_provider.get_credentials = Mock(return_value=credentials)

    dispatcher = Dispatcher(auth_provider, client)
    await dispatcher.patch("/accounts/invoices/1.json", {"name": "Test"})

    assert client.request.await_count == 1


async def test_not_required_account_slug_present() -> None:
    client = Mock()
    client.request = AsyncMock(return_value=httpx.Response(200, content=b""))

    auth_provider = Mock()
    auth_provider.reauth = AsyncMock()

    credentials = Mock()
    credentials.get_access_token = Mock(return_value="test")
    auth_provider.get_credentials = Mock(return_value=credentials)

    dispatcher = Dispatcher(auth_provider, client, "test")
    await dispatcher.patch("/accounts/invoices/1.json", {"name": "Test"})

    assert client.request.await_count == 1
