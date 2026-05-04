from unittest.mock import AsyncMock, Mock

import pytest

from fakturoid_sdk import FakturoidClient
from fakturoid_sdk.enums import InvoiceEvent
from fakturoid_sdk.exceptions import PdfNotReadyError


@pytest.fixture
def fakturoid() -> FakturoidClient:
    return FakturoidClient(
        client_id="id",
        client_secret="secret",
        user_agent="TestAgent",
        account_slug="slug",
    )


async def test_invoice_fire_action_sends_event_as_query_param(fakturoid: FakturoidClient) -> None:
    fakturoid.dispatcher.post = AsyncMock(return_value=Mock())
    fakturoid.dispatcher.post.return_value.get_status_code.return_value = 204
    fakturoid.dispatcher.post.return_value.get_body.return_value = {}

    await fakturoid.invoices.fire_action(123, event="lock")

    fakturoid.dispatcher.post.assert_awaited_with(
        "/accounts/{accountSlug}/invoices/123/fire.json",
        None,
        query_params={"event": "lock"},
    )


async def test_invoice_fire_typed_event_uses_value(fakturoid: FakturoidClient) -> None:
    fakturoid.dispatcher.post = AsyncMock(return_value=Mock())
    fakturoid.dispatcher.post.return_value.get_status_code.return_value = 204
    fakturoid.dispatcher.post.return_value.get_body.return_value = {}

    await fakturoid.invoices.fire(123, event=InvoiceEvent.LOCK)

    fakturoid.dispatcher.post.assert_awaited_with(
        "/accounts/{accountSlug}/invoices/123/fire.json",
        None,
        query_params={"event": "lock"},
    )


async def test_create_correction_sets_document_type_and_correction_id(
    fakturoid: FakturoidClient,
) -> None:
    fakturoid.dispatcher.post = AsyncMock(return_value=Mock())
    fakturoid.dispatcher.post.return_value.get_body.return_value = {"id": 456}

    await fakturoid.invoices.create_correction(123, {"lines": [{"name": "Test"}]})

    fakturoid.dispatcher.post.assert_awaited_with(
        "/accounts/{accountSlug}/invoices.json",
        {"lines": [{"name": "Test"}], "document_type": "correction", "correction_id": 123},
        query_params=None,
    )


async def test_get_pdf_or_none_returns_none_on_204(fakturoid: FakturoidClient) -> None:
    fakturoid.dispatcher.get = AsyncMock(return_value=Mock())
    fakturoid.dispatcher.get.return_value.get_status_code.return_value = 204

    result = await fakturoid.invoices.get_pdf_or_none(123)
    assert result is None


async def test_get_pdf_or_none_returns_bytes_on_200(fakturoid: FakturoidClient) -> None:
    fakturoid.dispatcher.get = AsyncMock(return_value=Mock())
    fakturoid.dispatcher.get.return_value.get_status_code.return_value = 200
    fakturoid.dispatcher.get.return_value.get_bytes.return_value = b"pdf_content"

    result = await fakturoid.invoices.get_pdf_or_none(123)
    assert result == b"pdf_content"


async def test_wait_for_pdf_retries_until_ready(fakturoid: FakturoidClient) -> None:
    fakturoid.invoices.get_pdf_or_none = AsyncMock(side_effect=[None, None, b"pdf_content"])

    result = await fakturoid.invoices.wait_for_pdf(123, delay_seconds=0)
    assert result == b"pdf_content"
    assert fakturoid.invoices.get_pdf_or_none.await_count == 3


async def test_wait_for_pdf_raises_after_attempts(fakturoid: FakturoidClient) -> None:
    fakturoid.invoices.get_pdf_or_none = AsyncMock(return_value=None)

    with pytest.raises(PdfNotReadyError):
        await fakturoid.invoices.wait_for_pdf(123, attempts=3, delay_seconds=0)

    assert fakturoid.invoices.get_pdf_or_none.await_count == 3
