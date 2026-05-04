from unittest.mock import AsyncMock, Mock

import httpx
import pytest

from fakturoid_sdk.dispatcher import Dispatcher
from fakturoid_sdk.exceptions import FakturoidSdkError


async def test_dispatcher_sends_user_agent_header() -> None:
    client = Mock()
    client.request = AsyncMock(return_value=httpx.Response(200, content=b"{}"))

    auth_provider = Mock()
    auth_provider.reauth = AsyncMock()
    credentials = Mock()
    credentials.get_access_token = Mock(return_value="test_token")
    auth_provider.get_credentials = Mock(return_value=credentials)

    user_agent = "TestApp (test@example.com)"
    dispatcher = Dispatcher(auth_provider, client, "test_slug", user_agent=user_agent)

    await dispatcher.get("/test")

    args, kwargs = client.request.call_args
    headers = kwargs.get("headers", {})
    assert headers.get("User-Agent") == user_agent


async def test_dispatcher_post_supports_query_params() -> None:
    client = Mock()
    client.request = AsyncMock(return_value=httpx.Response(200, content=b"{}"))

    auth_provider = Mock()
    auth_provider.reauth = AsyncMock()
    credentials = Mock()
    credentials.get_access_token = Mock(return_value="test_token")
    auth_provider.get_credentials = Mock(return_value=credentials)

    dispatcher = Dispatcher(auth_provider, client, "test_slug", user_agent="test")

    await dispatcher.post("/test", data={"key": "val"}, query_params={"q": "1"})

    args, kwargs = client.request.call_args
    url = kwargs.get("url") or args[1]
    assert "?q=1" in url
    assert kwargs.get("content") == b'{"key": "val"}'


async def test_required_account_slug_missing() -> None:
    client = Mock()
    client.request = AsyncMock()

    auth_provider = Mock()
    auth_provider.reauth = AsyncMock()
    auth_provider.get_credentials = Mock()

    dispatcher = Dispatcher(auth_provider, client, user_agent="test")

    with pytest.raises(
        FakturoidSdkError,
        match=r"Account slug is not set\. You must set it before calling this method\.",
    ):
        await dispatcher.patch("/accounts/{accountSlug}/invoices/1.json", {"name": "Test"})


async def test_required_account_slug_present() -> None:
    client = Mock()
    client.request = AsyncMock(return_value=httpx.Response(200, content=b""))

    auth_provider = Mock()
    auth_provider.reauth = AsyncMock()

    credentials = Mock()
    credentials.get_access_token = Mock(return_value="test")
    auth_provider.get_credentials = Mock(return_value=credentials)

    dispatcher = Dispatcher(auth_provider, client, "test", user_agent="test")
    await dispatcher.patch("/accounts/{accountSlug}/invoices/1.json", {"name": "Test"})

    assert client.request.await_count == 1


async def test_dispatcher_sends_empty_json_object_when_data_is_empty_dict() -> None:
    client = Mock()
    client.request = AsyncMock(return_value=httpx.Response(200, content=b"{}"))

    auth_provider = Mock()
    auth_provider.reauth = AsyncMock()
    credentials = Mock()
    credentials.get_access_token = Mock(return_value="test_token")
    auth_provider.get_credentials = Mock(return_value=credentials)

    dispatcher = Dispatcher(auth_provider, client, "test_slug", user_agent="test")

    await dispatcher.post("/test", data={})

    args, kwargs = client.request.call_args
    assert kwargs.get("content") == b"{}"


async def test_dispatcher_sends_no_body_when_data_is_none() -> None:
    client = Mock()
    client.request = AsyncMock(return_value=httpx.Response(200, content=b"{}"))

    auth_provider = Mock()
    auth_provider.reauth = AsyncMock()
    credentials = Mock()
    credentials.get_access_token = Mock(return_value="test_token")
    auth_provider.get_credentials = Mock(return_value=credentials)

    dispatcher = Dispatcher(auth_provider, client, "test_slug", user_agent="test")

    await dispatcher.post("/test", data=None)

    args, kwargs = client.request.call_args
    assert kwargs.get("content") is None
