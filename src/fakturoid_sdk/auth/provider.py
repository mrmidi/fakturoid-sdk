from __future__ import annotations

import base64
import json
from datetime import datetime, timedelta, timezone
from typing import Any, Protocol

import httpx

from ..exceptions import (
    AuthorizationFailedError,
    ClientError,
    ConnectionFailedError,
    InvalidDataError,
    RequestInfo,
    ServerError,
)
from ..response import Response
from .models import AccessToken, AuthType, CredentialCallback, Credentials


class AuthProviderProtocol(Protocol):
    """Protocol defining the interface for authentication providers."""

    async def reauth(self) -> Credentials | None:
        """Refreshes authentication if needed."""
        ...

    def get_credentials(self) -> Credentials | None:
        """Returns current credentials."""
        ...


class AuthProvider:
    """Handles OAuth2 authentication and token management for Fakturoid.

    Attributes:
        BASE_URL: The default base URL for Fakturoid API.
    """

    BASE_URL = "https://app.fakturoid.cz/api/v3"

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str | None,
        client: httpx.AsyncClient,
        *,
        base_url: str = BASE_URL,
    ) -> None:
        """Initializes the AuthProvider.

        Args:
            client_id: The OAuth2 client ID.
            client_secret: The OAuth2 client secret.
            redirect_uri: The OAuth2 redirect URI.
            client: The HTTPX async client to use for requests.
            base_url: The base URL for authentication requests.
        """
        self._client_id = client_id
        self._client_secret = client_secret
        self._redirect_uri = redirect_uri
        self._client = client
        self._base_url = base_url

        self._code: str | None = None
        self._credentials: Credentials | None = None
        self._credentials_callback: CredentialCallback | None = None

    def get_authentication_url(self, state: str | None = None) -> str:
        """Generates the URL for the user to authorize the application.

        Args:
            state: An optional state parameter to prevent CSRF.

        Returns:
            The authentication URL.
        """
        params: dict[str, str | None] = {
            "client_id": self._client_id,
            "redirect_uri": self._redirect_uri,
            "response_type": "code",
        }
        if state is not None:
            params["state"] = state

        # Mirror http_build_query-ish behavior: omit None values.
        query_parts: list[str] = []
        for key, value in params.items():
            if value is None:
                continue
            query_parts.append(f"{httpx.QueryParams({key: value})}")
        query = "&".join(query_parts)
        return f"{self._base_url}/oauth?{query}"

    def load_code(self, code: str) -> None:
        """Loads the authorization code obtained from the redirect.

        Args:
            code: The authorization code.
        """
        self._code = code

    def get_credentials(self) -> Credentials | None:
        """Returns the current credentials."""
        return self._credentials

    def set_credentials(self, credentials: Credentials | None) -> None:
        """Sets the current credentials.

        Args:
            credentials: The credentials to set.
        """
        self._credentials = credentials

    def set_credentials_callback(self, callback: CredentialCallback) -> None:
        """Sets a callback to be called when credentials are updated.

        Args:
            callback: A callable that accepts Credentials.
        """
        self._credentials_callback = callback

    async def request_credentials(self, code: str) -> None:
        """Requests credentials using an authorization code.

        Args:
            code: The authorization code.
        """
        self.load_code(code)
        await self.auth(AuthType.AUTHORIZATION_CODE_FLOW)

    async def auth(
        self,
        auth_type: AuthType = AuthType.AUTHORIZATION_CODE_FLOW,
        credentials: Credentials | None = None,
    ) -> Credentials | None:
        """Performs authentication.

        Args:
            auth_type: The authentication flow to use.
            credentials: Optional existing credentials to use.

        Returns:
            The obtained credentials.
        """
        self._credentials = credentials
        if auth_type is AuthType.AUTHORIZATION_CODE_FLOW:
            return await self._authorization_code()
        return await self._client_credentials()

    async def reauth(self) -> Credentials | None:
        """Refreshes the authentication if the current token is expired.

        Returns:
            The refreshed or current credentials.

        Raises:
            AuthorizationFailedError: If re-authentication fails or credentials are invalid.
        """
        credentials = self.get_credentials()
        if (
            credentials is None
            or not credentials.get_access_token()
            or (
                credentials.get_auth_type() is AuthType.AUTHORIZATION_CODE_FLOW
                and not credentials.get_refresh_token()
            )
        ):
            raise AuthorizationFailedError("Invalid credentials")

        if not credentials.is_expired():
            return credentials

        if credentials.get_auth_type() is AuthType.AUTHORIZATION_CODE_FLOW:
            return await self.oauth2_refresh()

        return await self.auth(AuthType.CLIENT_CREDENTIALS_CODE_FLOW)

    async def oauth2_refresh(self) -> Credentials | None:
        """Refreshes the OAuth2 access token using a refresh token.

        Returns:
            The refreshed credentials.

        Raises:
            AuthorizationFailedError: If the refresh request fails.
        """
        if self._credentials is None:
            return None

        refresh_token = self._credentials.get_refresh_token()
        try:
            access_token = await self._make_request(
                {"grant_type": "refresh_token", "refresh_token": refresh_token}
            )
        except (InvalidDataError, ConnectionFailedError) as exc:
            raise AuthorizationFailedError(
                f"Error occurred while refreshing token. Message: {exc}"
            ) from exc
        except (ClientError, ServerError) as exc:
            # Mirror PHP behavior: use reason phrase if possible.
            message = exc.response.original.reason_phrase or ""
            raise AuthorizationFailedError(f"Error occurred. Message: {message}") from exc

        expires_in = max(0, access_token.expires_in - 10)
        expire_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
        self._credentials = Credentials(
            refresh_token=access_token.refresh_token or refresh_token,
            access_token=access_token.access_token,
            expire_at=expire_at,
            auth_type=self._credentials.get_auth_type(),
        )
        self._call_credentials_callback()
        return self._credentials

    async def revoke(self) -> bool:
        """Revokes the current refresh token.

        Returns:
            True if revocation was successful.

        Raises:
            AuthorizationFailedError: If revocation is not supported or fails.
            ConnectionFailedError: If a connection error occurs.
            ClientError: If the server returns a 4xx error.
            ServerError: If the server returns a 5xx error.
        """
        if self._credentials is None:
            raise AuthorizationFailedError("Load authentication screen first.")
        if self._credentials.get_auth_type() is not AuthType.AUTHORIZATION_CODE_FLOW:
            raise AuthorizationFailedError("Revoke is only available for authorization code flow")

        url = f"{self._base_url}/oauth/revoke"
        auth = base64.b64encode(f"{self._client_id}:{self._client_secret}".encode()).decode(
            "ascii"
        )
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Basic {auth}",
        }
        body = json.dumps({"token": self._credentials.get_refresh_token()}).encode("utf-8")
        request_info = RequestInfo(method="POST", url=url, headers=headers, body=body)

        try:
            response = await self._client.post(url, headers=headers, content=body)
        except httpx.RequestError as exc:
            raise ConnectionFailedError(str(exc)) from exc

        wrapped = Response(response)
        status = wrapped.get_status_code()
        if 400 <= status < 500:
            raise ClientError(
                response.reason_phrase or "",
                status_code=status,
                request=request_info,
                response=wrapped,
            )
        if 500 <= status < 600:
            raise ServerError(
                response.reason_phrase or "",
                status_code=status,
                request=request_info,
                response=wrapped,
            )
        return status == 200

    async def _authorization_code(self) -> Credentials | None:
        """Internal method for Authorization Code flow."""
        if self._credentials is not None:
            return self._credentials
        if not self._code:
            raise AuthorizationFailedError("Load authentication screen first.")

        try:
            access_token = await self._make_request(
                {
                    "grant_type": "authorization_code",
                    "code": self._code,
                    "redirect_uri": self._redirect_uri,
                }
            )
        except (InvalidDataError, ConnectionFailedError) as exc:
            raise AuthorizationFailedError(
                f"An error occurred while authorization code flow. Message: {exc}"
            ) from exc
        except (ClientError, ServerError) as exc:
            message = exc.response.original.reason_phrase or ""
            raise AuthorizationFailedError(f"Error occurred. Message: {message}") from exc

        expires_in = max(0, access_token.expires_in - 10)
        expire_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
        self._credentials = Credentials(
            refresh_token=access_token.refresh_token,
            access_token=access_token.access_token,
            expire_at=expire_at,
            auth_type=AuthType.AUTHORIZATION_CODE_FLOW,
        )
        self._call_credentials_callback()
        return self._credentials

    async def _client_credentials(self) -> Credentials | None:
        """Internal method for Client Credentials flow."""
        try:
            access_token = await self._make_request({"grant_type": "client_credentials"})
        except (InvalidDataError, ConnectionFailedError) as exc:
            raise AuthorizationFailedError(
                f"An error occurred while client credentials flow. Message: {exc}"
            ) from exc
        except (ClientError, ServerError) as exc:
            message = exc.response.original.reason_phrase or ""
            raise AuthorizationFailedError(f"Error occurred. Message: {message}") from exc

        expires_in = max(0, access_token.expires_in - 10)
        expire_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
        self._credentials = Credentials(
            refresh_token=access_token.refresh_token,
            access_token=access_token.access_token,
            expire_at=expire_at,
            auth_type=AuthType.CLIENT_CREDENTIALS_CODE_FLOW,
        )
        self._call_credentials_callback()
        return self._credentials

    def _call_credentials_callback(self) -> None:
        """Calls the credentials callback if set."""
        if self._credentials_callback is not None:
            self._credentials_callback(self._credentials)

    async def _make_request(self, body: dict[str, Any]) -> AccessToken:
        """Internal method to make OAuth2 token requests."""
        url = f"{self._base_url}/oauth/token"
        auth = base64.b64encode(f"{self._client_id}:{self._client_secret}".encode()).decode(
            "ascii"
        )
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Basic {auth}",
        }

        try:
            payload = json.dumps(body).encode("utf-8")
        except TypeError as exc:
            raise InvalidDataError(
                f"Error occurred while decoding response. Message: {exc}"
            ) from exc

        request_info = RequestInfo(method="POST", url=url, headers=headers, body=payload)

        try:
            response = await self._client.post(url, headers=headers, content=payload)
        except httpx.RequestError as exc:
            raise ConnectionFailedError(f"Error occurred. Message: {exc}") from exc

        wrapped = Response(response)
        status = wrapped.get_status_code()

        if 400 <= status < 500:
            raise ClientError(
                response.reason_phrase or "",
                status_code=status,
                request=request_info,
                response=wrapped,
            )
        if 500 <= status < 600:
            raise ServerError(
                response.reason_phrase or "",
                status_code=status,
                request=request_info,
                response=wrapped,
            )

        try:
            body_json = wrapped.get_body(return_json_as_dict=True)
        except Exception as exc:
            raise InvalidDataError(
                f"Error occurred while decoding response. Message: {exc}"
            ) from exc

        if not isinstance(body_json, dict):
            raise InvalidDataError("Error occurred while processing response.")

        if isinstance(body_json.get("error"), str):
            raise InvalidDataError(f"Error: {body_json['error']}")

        grant_type = body.get("grant_type")
        if grant_type in {"client_credentials", "refresh_token"}:
            auth_type = AuthType.CLIENT_CREDENTIALS_CODE_FLOW
        else:
            auth_type = AuthType.AUTHORIZATION_CODE_FLOW

        try:
            return AccessToken.create(body_json, auth_type)
        except ValueError as exc:
            raise AuthorizationFailedError(
                f"Error occurred while processing response. Message: {exc}"
            ) from exc
