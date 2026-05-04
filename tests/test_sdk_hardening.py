"""Tests for SDK hardening: User-Agent propagation, exports, and validation."""
from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest

from fakturoid_sdk import FakturoidClient
from fakturoid_sdk.auth.models import AuthType, Credentials
from fakturoid_sdk.auth.provider import AuthProvider

# ---------------------------------------------------------------------------
# User-Agent validation
# ---------------------------------------------------------------------------


def test_empty_user_agent_raises_value_error() -> None:
    with pytest.raises(ValueError, match="user_agent must be a non-empty string"):
        FakturoidClient(
            client_id="id",
            client_secret="secret",
            user_agent="",
            account_slug="slug",
        )


def test_whitespace_only_user_agent_raises_value_error() -> None:
    with pytest.raises(ValueError, match="user_agent must be a non-empty string"):
        FakturoidClient(
            client_id="id",
            client_secret="secret",
            user_agent="   ",
            account_slug="slug",
        )


# ---------------------------------------------------------------------------
# User-Agent wiring: FakturoidClient forwards to auth + dispatcher
# ---------------------------------------------------------------------------


def test_client_wires_user_agent_to_auth_and_dispatcher() -> None:
    client = FakturoidClient(
        client_id="id",
        client_secret="secret",
        user_agent="TestApp (test@example.com)",
        account_slug="slug",
    )
    assert client.auth._user_agent == "TestApp (test@example.com)"
    assert client.dispatcher._user_agent == "TestApp (test@example.com)"


# ---------------------------------------------------------------------------
# User-Agent in OAuth token requests
# ---------------------------------------------------------------------------


async def test_auth_token_request_includes_user_agent() -> None:
    """AuthProvider._make_request() must include User-Agent header."""
    import httpx

    provider = AuthProvider(
        "id", "secret", None, AsyncMock(),
        user_agent="TestApp (test@example.com)",
    )
    mock_response = httpx.Response(
        200,
        headers={"Content-Type": "application/json"},
        content=b'{"access_token":"tok","token_type":"bearer","expires_in":7200}',
    )
    provider._client.post = AsyncMock(return_value=mock_response)

    token = await provider._make_request({"grant_type": "client_credentials"})
    assert token.access_token == "tok"

    call_kwargs = provider._client.post.call_args
    headers = call_kwargs.kwargs.get("headers") or call_kwargs[1].get("headers", {})
    assert headers.get("User-Agent") == "TestApp (test@example.com)"


# ---------------------------------------------------------------------------
# User-Agent in OAuth revoke requests
# ---------------------------------------------------------------------------


async def test_auth_revoke_request_includes_user_agent() -> None:
    """AuthProvider.revoke() must include User-Agent header."""
    import httpx

    provider = AuthProvider(
        "id", "secret", "http://localhost", AsyncMock(),
        user_agent="TestApp (test@example.com)",
    )
    provider.set_credentials(
        Credentials(
            refresh_token="refresh",
            access_token="access",
            expire_at=datetime.now(timezone.utc),
            auth_type=AuthType.AUTHORIZATION_CODE_FLOW,
        )
    )

    mock_response = httpx.Response(
        200,
        headers={"Content-Type": "application/json"},
        content=b"{}",
    )
    provider._client.post = AsyncMock(return_value=mock_response)

    result = await provider.revoke()
    assert result is True

    call_kwargs = provider._client.post.call_args
    headers = call_kwargs.kwargs.get("headers") or call_kwargs[1].get("headers", {})
    assert headers.get("User-Agent") == "TestApp (test@example.com)"


# ---------------------------------------------------------------------------
# Root export
# ---------------------------------------------------------------------------


def test_pdfnotreadyerror_importable_from_root() -> None:
    from fakturoid_sdk import PdfNotReadyError as PdfErr

    err = PdfErr(123, attempts=5)
    assert err.invoice_id == 123
    assert err.attempts == 5
    assert "after 5 attempts" in str(err)


def test_pdfnotreadyerror_without_attempts() -> None:
    from fakturoid_sdk import PdfNotReadyError as PdfErr

    err = PdfErr(42)
    assert err.invoice_id == 42
    assert err.attempts is None
    assert "is not ready" in str(err)
    assert "attempts" not in str(err)


# ---------------------------------------------------------------------------
# InvoiceEvent.PAY removed
# ---------------------------------------------------------------------------


def test_invoice_event_pay_removed() -> None:
    from fakturoid_sdk.enums import InvoiceEvent

    assert not hasattr(InvoiceEvent, "PAY")


def test_invoice_event_still_has_valid_events() -> None:
    from fakturoid_sdk.enums import InvoiceEvent

    assert InvoiceEvent.LOCK.value == "lock"
    assert InvoiceEvent.UNLOCK.value == "unlock"
    assert InvoiceEvent.MARK_AS_SENT.value == "mark_as_sent"
    assert InvoiceEvent.CANCEL.value == "cancel"
    assert InvoiceEvent.UNDO_CANCEL.value == "undo_cancel"
    assert InvoiceEvent.MARK_AS_UNCOLLECTIBLE.value == "mark_as_uncollectible"
    assert InvoiceEvent.UNDO_UNCOLLECTIBLE.value == "undo_uncollectible"
