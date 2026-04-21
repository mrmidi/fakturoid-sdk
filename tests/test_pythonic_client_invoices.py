from unittest.mock import AsyncMock, Mock

import httpx

from fakturoid_sdk.client import Invoices
from fakturoid_sdk.response import Response


def _json_response(payload: bytes) -> Response:
    return Response(
        httpx.Response(
            200,
            headers={"Content-Type": "application/json"},
            content=payload,
        )
    )


def _bytes_response(payload: bytes) -> Response:
    return Response(httpx.Response(200, content=payload))


async def test_invoices_list_uses_keyword_params() -> None:
    dispatcher = Mock()
    dispatcher.get = AsyncMock(return_value=_json_response(b"{}"))

    invoices = Invoices(dispatcher)
    result = await invoices.list(page=2, status="open")

    assert result == {}
    dispatcher.get.assert_awaited_once_with(
        "/accounts/{accountSlug}/invoices.json",
        {"page": 2, "status": "open"},
    )


async def test_invoices_get_pdf_returns_bytes() -> None:
    dispatcher = Mock()
    dispatcher.get = AsyncMock(return_value=_bytes_response(b"%PDF..."))

    invoices = Invoices(dispatcher)
    data = await invoices.get_pdf(123)

    assert data == b"%PDF..."
    dispatcher.get.assert_awaited_once_with(
        "/accounts/{accountSlug}/invoices/123/download.pdf",
        None,
    )
