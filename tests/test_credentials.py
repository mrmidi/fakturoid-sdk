from __future__ import annotations

from datetime import datetime, timedelta, timezone

from fakturoid_sdk.auth import AuthType, Credentials


def test_credentials_roundtrip_and_expiration() -> None:
    expire_at = datetime.fromisoformat("2021-01-01T00:00:00+00:00")
    credentials = Credentials(
        refresh_token="refresh_token",
        access_token="access_token",
        expire_at=expire_at,
        auth_type=AuthType.AUTHORIZATION_CODE_FLOW,
    )

    assert credentials.get_access_token() == "access_token"
    assert credentials.get_refresh_token() == "refresh_token"
    assert credentials.get_auth_type().value == AuthType.AUTHORIZATION_CODE_FLOW.value

    assert credentials.is_expired() is True
    assert credentials.get_expire_at().isoformat() == "2021-01-01T00:00:00+00:00"

    expected_json = (
        '{"refreshToken":"refresh_token","accessToken":"access_token",'
        '"expireAt":"2021-01-01T00:00:00+00:00","authType":"authorization_code"}'
    )
    assert credentials.to_json() == expected_json

    credentials.set_auth_type(AuthType.CLIENT_CREDENTIALS_CODE_FLOW)
    assert credentials.get_auth_type().value == AuthType.CLIENT_CREDENTIALS_CODE_FLOW.value


def test_switch_auth_type() -> None:
    credentials = Credentials(
        refresh_token="refresh_token",
        access_token="access_token",
        expire_at=datetime.now(timezone.utc),
        auth_type=AuthType.AUTHORIZATION_CODE_FLOW,
    )

    credentials.set_auth_type(AuthType.CLIENT_CREDENTIALS_CODE_FLOW)
    assert credentials.get_auth_type().value == AuthType.CLIENT_CREDENTIALS_CODE_FLOW.value


def test_expiration() -> None:
    expire_at = datetime.now(timezone.utc) + timedelta(seconds=7200)
    credentials = Credentials(
        refresh_token="refresh_token",
        access_token="access_token",
        expire_at=expire_at,
        auth_type=AuthType.CLIENT_CREDENTIALS_CODE_FLOW,
    )
    assert credentials.is_expired() is False

    expire_at = datetime.now(timezone.utc) - timedelta(seconds=10)
    credentials = Credentials(
        refresh_token="refresh_token",
        access_token="access_token",
        expire_at=expire_at,
        auth_type=AuthType.CLIENT_CREDENTIALS_CODE_FLOW,
    )
    assert credentials.is_expired() is True
