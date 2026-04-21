from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any
from unittest.mock import Mock

import httpx
import pytest

from fakturoid_sdk.auth import AuthProvider, AuthType, Credentials
from fakturoid_sdk.exceptions import AuthorizationFailedError, ClientError, ServerError


def _client_with_transport(handler: Any) -> httpx.AsyncClient:
    transport = httpx.MockTransport(handler)
    return httpx.AsyncClient(transport=transport)


@pytest.mark.asyncio
async def test_authentication_url_with_state() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:  # pragma: no cover
        raise AssertionError("Should not be called")

    async with _client_with_transport(handler) as client:
        auth_provider = AuthProvider("clientId", "clientSecret", "redirectUri", client)

        base_url = "https://app.fakturoid.cz/api/v3/oauth"
        expected = (
            base_url
            + "?client_id=clientId&redirect_uri=redirectUri&response_type=code&state=c"
        )
        assert auth_provider.get_authentication_url("c") == expected


@pytest.mark.asyncio
async def test_authentication_url_without_state() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:  # pragma: no cover
        raise AssertionError("Should not be called")

    async with _client_with_transport(handler) as client:
        auth_provider = AuthProvider("clientId", "clientSecret", "redirectUri", client)
        assert (
            auth_provider.get_authentication_url()
            == "https://app.fakturoid.cz/api/v3/oauth?client_id=clientId&redirect_uri=redirectUri&response_type=code"
        )


@pytest.mark.asyncio
async def test_empty_credentials_reauth() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:  # pragma: no cover
        raise AssertionError("Should not be called")

    async with _client_with_transport(handler) as client:
        auth_provider = AuthProvider("clientId", "clientSecret", None, client)

        with pytest.raises(AuthorizationFailedError, match=r"Invalid credentials"):
            await auth_provider.reauth()


@pytest.mark.asyncio
async def test_authorization_code_reauth_with_empty_refresh_token() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:  # pragma: no cover
        raise AssertionError("Should not be called")

    async with _client_with_transport(handler) as client:
        auth_provider = AuthProvider("clientId", "clientSecret", None, client)
        credentials = Credentials(
            refresh_token=None,
            access_token="access_token",
            expire_at=datetime.now(timezone.utc) - timedelta(seconds=1),
            auth_type=AuthType.AUTHORIZATION_CODE_FLOW,
        )
        auth_provider.set_credentials(credentials)

        with pytest.raises(AuthorizationFailedError, match=r"Invalid credentials"):
            await auth_provider.reauth()


@pytest.mark.asyncio
async def test_authorization_code_reauth_refreshes_and_calls_callback() -> None:
    called = Mock()

    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url == httpx.URL("https://app.fakturoid.cz/api/v3/oauth/token")
        return httpx.Response(
            200,
            headers={"Content-Type": "application/json"},
            json={"refresh_token": "", "access_token": "access_token", "expires_in": 7200},
        )

    async with _client_with_transport(handler) as client:
        auth_provider = AuthProvider("clientId", "clientSecret", None, client)
        auth_provider.set_credentials_callback(called)
        credentials = Credentials(
            refresh_token="refresh_token",
            access_token="access_token",
            expire_at=datetime.now(timezone.utc) - timedelta(seconds=1),
            auth_type=AuthType.AUTHORIZATION_CODE_FLOW,
        )
        auth_provider.set_credentials(credentials)

        await auth_provider.reauth()
        called.assert_called_once()


@pytest.mark.asyncio
async def test_reauth_refresh_with_error_response() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            headers={"Content-Type": "application/json"},
            json={"error": "invalid_grant"},
        )

    async with _client_with_transport(handler) as client:
        auth_provider = AuthProvider("clientId", "clientSecret", None, client)
        credentials = Credentials(
            refresh_token="refresh_token",
            access_token="access_token",
            expire_at=datetime.now(timezone.utc) - timedelta(seconds=1),
            auth_type=AuthType.AUTHORIZATION_CODE_FLOW,
        )
        auth_provider.set_credentials(credentials)

        with pytest.raises(
            AuthorizationFailedError,
            match=r"Error occurred while refreshing token\. Message: Error: invalid_grant",
        ):
            await auth_provider.reauth()


@pytest.mark.asyncio
async def test_reauth_refresh_without_access_token_in_response() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, headers={"Content-Type": "application/json"}, json={})

    async with _client_with_transport(handler) as client:
        auth_provider = AuthProvider("clientId", "clientSecret", None, client)
        credentials = Credentials(
            refresh_token="refresh_token",
            access_token="access_token",
            expire_at=datetime.now(timezone.utc) - timedelta(seconds=1),
            auth_type=AuthType.AUTHORIZATION_CODE_FLOW,
        )
        auth_provider.set_credentials(credentials)

        with pytest.raises(
            AuthorizationFailedError,
            match=r"Invalid or missing \"access_token\"\. Expected string, got NoneType\.",
        ):
            await auth_provider.reauth()


@pytest.mark.asyncio
async def test_client_credentials_flow() -> None:
    called = Mock()

    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            headers={"Content-Type": "application/json"},
            json={"refresh_token": "", "access_token": "access_token", "expires_in": 7200},
        )

    async with _client_with_transport(handler) as client:
        auth_provider = AuthProvider("clientId", "clientSecret", None, client)
        auth_provider.set_credentials_callback(called)

        credentials = await auth_provider.auth(AuthType.CLIENT_CREDENTIALS_CODE_FLOW)
        assert isinstance(credentials, Credentials)
        assert credentials.get_access_token() == "access_token"
        assert credentials.get_refresh_token() is None
        assert credentials.get_auth_type() is AuthType.CLIENT_CREDENTIALS_CODE_FLOW

        called.assert_called_once()


@pytest.mark.asyncio
async def test_client_credentials_empty_response() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, headers={"Content-Type": "application/json"}, json={})

    async with _client_with_transport(handler) as client:
        auth_provider = AuthProvider("clientId", "clientSecret", None, client)

        with pytest.raises(
            AuthorizationFailedError,
            match=r"Error occurred while processing response\.",
        ):
            await auth_provider.auth(AuthType.CLIENT_CREDENTIALS_CODE_FLOW)


@pytest.mark.asyncio
async def test_authorization_code_without_code() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:  # pragma: no cover
        raise AssertionError("Should not be called")

    async with _client_with_transport(handler) as client:
        auth_provider = AuthProvider("clientId", "clientSecret", None, client)

        with pytest.raises(AuthorizationFailedError, match=r"Load authentication screen first\."):
            await auth_provider.auth(AuthType.AUTHORIZATION_CODE_FLOW)


@pytest.mark.asyncio
async def test_revoke() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.url == httpx.URL("https://app.fakturoid.cz/api/v3/oauth/revoke")
        return httpx.Response(200, headers={"Content-Type": "application/json"}, json={})

    async with _client_with_transport(handler) as client:
        auth_provider = AuthProvider("clientId", "clientSecret", None, client)
        auth_provider.set_credentials(
            Credentials(
                refresh_token="refresh_token",
                access_token="access_token",
                expire_at=datetime.now(timezone.utc) + timedelta(seconds=3600),
                auth_type=AuthType.AUTHORIZATION_CODE_FLOW,
            )
        )

        assert await auth_provider.revoke() is True


@pytest.mark.asyncio
async def test_revoke_500_raises_server_error() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, headers={"Content-Type": "application/json"}, json={})

    async with _client_with_transport(handler) as client:
        auth_provider = AuthProvider("clientId", "clientSecret", None, client)
        auth_provider.set_credentials(
            Credentials(
                refresh_token="refresh_token",
                access_token="access_token",
                expire_at=datetime.now(timezone.utc) + timedelta(seconds=3600),
                auth_type=AuthType.AUTHORIZATION_CODE_FLOW,
            )
        )

        with pytest.raises(ServerError):
            await auth_provider.revoke()


@pytest.mark.asyncio
async def test_revoke_400_raises_client_error() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(400, headers={"Content-Type": "application/json"}, json={})

    async with _client_with_transport(handler) as client:
        auth_provider = AuthProvider("clientId", "clientSecret", None, client)
        auth_provider.set_credentials(
            Credentials(
                refresh_token="refresh_token",
                access_token="access_token",
                expire_at=datetime.now(timezone.utc) + timedelta(seconds=3600),
                auth_type=AuthType.AUTHORIZATION_CODE_FLOW,
            )
        )

        with pytest.raises(ClientError):
            await auth_provider.revoke()


@pytest.mark.asyncio
async def test_revoke_client_credentials_flow_not_allowed() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:  # pragma: no cover
        raise AssertionError("Should not be called")

    async with _client_with_transport(handler) as client:
        auth_provider = AuthProvider("clientId", "clientSecret", None, client)
        auth_provider.set_credentials(
            Credentials(
                refresh_token=None,
                access_token="access_token",
                expire_at=datetime.now(timezone.utc) + timedelta(seconds=3600),
                auth_type=AuthType.CLIENT_CREDENTIALS_CODE_FLOW,
            )
        )

        with pytest.raises(
            AuthorizationFailedError,
            match=r"Revoke is only available for authorization code flow",
        ):
            await auth_provider.revoke()


@pytest.mark.asyncio
async def test_revoke_without_credentials() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:  # pragma: no cover
        raise AssertionError("Should not be called")

    async with _client_with_transport(handler) as client:
        auth_provider = AuthProvider("clientId", "clientSecret", None, client)

        with pytest.raises(AuthorizationFailedError, match=r"Load authentication screen first\."):
            await auth_provider.revoke()


@pytest.mark.asyncio
async def test_authorization_code_simple_request_credentials() -> None:
    called = Mock()

    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            headers={"Content-Type": "application/json"},
            json={
                "refresh_token": "refresh_token",
                "access_token": "access_token",
                "expires_in": 7200,
            },
        )

    async with _client_with_transport(handler) as client:
        auth_provider = AuthProvider("clientId", "clientSecret", "redirectUri", client)
        auth_provider.set_credentials_callback(called)

        await auth_provider.request_credentials("CODE")
        credentials = auth_provider.get_credentials()

        assert isinstance(credentials, Credentials)
        assert credentials.get_access_token() == "access_token"
        assert credentials.get_refresh_token() == "refresh_token"
        assert credentials.get_auth_type() is AuthType.AUTHORIZATION_CODE_FLOW

        called.assert_called_once()


@pytest.mark.asyncio
async def test_authorization_invalid_response() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, headers={"Content-Type": "application/json"}, json={})

    async with _client_with_transport(handler) as client:
        auth_provider = AuthProvider("clientId", "clientSecret", "redirectUri", client)

        with pytest.raises(
            AuthorizationFailedError,
            match=r"Error occurred while processing response\.",
        ):
            await auth_provider.request_credentials("CODE")


@pytest.mark.asyncio
async def test_authorization_request_error() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("test", request=request)

    async with _client_with_transport(handler) as client:
        auth_provider = AuthProvider("clientId", "clientSecret", "redirectUri", client)

        with pytest.raises(
            AuthorizationFailedError,
            match=r"An error occurred while authorization code flow\.",
        ):
            await auth_provider.request_credentials("CODE")
