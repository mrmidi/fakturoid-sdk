from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from ..exceptions import InvalidDataError


class AuthType(str, Enum):
    """Supported OAuth2 authentication flows."""

    AUTHORIZATION_CODE_FLOW = "authorization_code"
    CLIENT_CREDENTIALS_CODE_FLOW = "client_credentials"


@dataclass(slots=True)
class Credentials:
    """OAuth2 credentials storage.

    Attributes:
        refresh_token: The token used to refresh the access token.
        access_token: The token used for authenticated requests.
        expire_at: The timestamp when the access token expires.
        auth_type: The authentication flow used to obtain these credentials.
    """

    refresh_token: str | None
    access_token: str | None
    expire_at: datetime
    auth_type: AuthType

    def get_refresh_token(self) -> str | None:
        """Returns the refresh token."""
        return self.refresh_token

    def get_access_token(self) -> str | None:
        """Returns the access token."""
        return self.access_token

    def is_expired(self) -> bool:
        """Checks if the access token has expired.

        Returns:
            True if the token is expired, False otherwise.
        """
        now = datetime.now(timezone.utc)
        expire_at = self.expire_at
        if expire_at.tzinfo is None:
            expire_at = expire_at.replace(tzinfo=timezone.utc)
        return now > expire_at

    def get_auth_type(self) -> AuthType:
        """Returns the authentication type."""
        return self.auth_type

    def set_auth_type(self, auth_type: AuthType) -> None:
        """Sets the authentication type."""
        self.auth_type = auth_type

    def get_expire_at(self) -> datetime:
        """Returns the expiration timestamp."""
        return self.expire_at

    def to_json(self) -> str:
        """Encodes the credentials as a JSON string.

        Returns:
            A JSON string representation of the credentials.

        Raises:
            InvalidDataError: If encoding to JSON fails.
        """
        try:
            expire_at = self.expire_at
            if expire_at.tzinfo is None:
                expire_at = expire_at.replace(tzinfo=timezone.utc)
            return json.dumps(
                {
                    "refreshToken": self.refresh_token,
                    "accessToken": self.access_token,
                    "expireAt": expire_at.isoformat(),
                    "authType": self.auth_type.value,
                },
                separators=(",", ":"),
            )
        except Exception as exc:  # pragma: no cover
            raise InvalidDataError("Failed to encode credentials to JSON") from exc


CredentialCallback = Callable[[Credentials | None], None]


@dataclass(frozen=True, slots=True)
class AccessToken:
    """Represents an OAuth2 access token response.

    Attributes:
        access_token: The access token string.
        token_type: The type of the token (usually 'Bearer').
        expires_in: Number of seconds until expiration.
        refresh_token: The refresh token string, if provided.
        scope: The scopes granted to the token.
        auth_type: The authentication flow used.
    """

    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str | None
    scope: str | None
    auth_type: AuthType

    @classmethod
    def create(cls, data: dict[str, Any], auth_type: AuthType) -> AccessToken:
        """Creates an AccessToken from a dictionary.

        Args:
            data: The dictionary containing the token response.
            auth_type: The authentication flow used.

        Returns:
            An AccessToken instance.

        Raises:
            ValueError: If the input data is invalid.
        """
        access_token = data.get("access_token")
        if not isinstance(access_token, str) or access_token == "":
            actual_type = type(access_token).__name__
            raise ValueError(
                f'Invalid or missing "access_token". Expected string, got {actual_type}.'
            )

        token_type = data.get("token_type", "Bearer")
        if not isinstance(token_type, str):
            raise ValueError(
                f'Invalid "token_type". Expected string, got {type(token_type).__name__}.'
            )

        expires_in_raw = data.get("expires_in", 0)
        if isinstance(expires_in_raw, bool) or (
            not isinstance(expires_in_raw, int) and not isinstance(expires_in_raw, str)
        ):
            raise ValueError(
                f'Invalid "expires_in". Expected integer, got {type(expires_in_raw).__name__}.'
            )
        try:
            expires_in = int(expires_in_raw)
        except ValueError as exc:
            raise ValueError(
                f'Invalid "expires_in". Expected integer, got {type(expires_in_raw).__name__}.'
            ) from exc

        scope = data.get("scope")
        if scope is not None and not isinstance(scope, str):
            actual_type = type(scope).__name__
            raise ValueError(
                f'Invalid "scope". Expected string or null, got {actual_type}.'
            )

        raw_refresh = data.get("refresh_token")
        final_refresh: str | None = None
        if auth_type is AuthType.AUTHORIZATION_CODE_FLOW:
            if not isinstance(raw_refresh, str) or raw_refresh == "":
                raise ValueError(
                    "Refresh token is required and must be a string for Authorization Code Flow."
                )
            final_refresh = raw_refresh

        return cls(
            access_token=access_token,
            token_type=token_type,
            expires_in=expires_in,
            refresh_token=final_refresh,
            scope=scope,
            auth_type=auth_type,
        )
