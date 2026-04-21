import datetime as dt
import json
from unittest.mock import AsyncMock, Mock, call

import httpx

from fakturoid_sdk.client import Invoices
from fakturoid_sdk.enums import InvoiceEvent, InvoiceStatus
from fakturoid_sdk.models import Invoice as InvoiceModel
from fakturoid_sdk.response import Response


def _json_response(payload: object) -> Response:
    return Response(
        httpx.Response(
            200,
            headers={"Content-Type": "application/json"},
            content=json.dumps(payload).encode("utf-8"),
        )
    )


async def test_invoices_list_coerces_date_and_enum() -> None:
    dispatcher = Mock()
    dispatcher.get = AsyncMock(return_value=_json_response({}))

    invoices = Invoices(dispatcher)
    result = await invoices.list(
        since=dt.date(2026, 1, 1),
        status=InvoiceStatus.OPEN,
        page=2,
    )

    assert result == {}
    dispatcher.get.assert_awaited_once_with(
        "/accounts/{accountSlug}/invoices.json",
        {"since": "2026-01-01", "status": "open", "page": 2},
    )


async def test_invoices_fire_accepts_enum() -> None:
    dispatcher = Mock()
    dispatcher.post = AsyncMock(return_value=_json_response({}))

    invoices = Invoices(dispatcher)
    result = await invoices.fire(123, event=InvoiceEvent.PAY)

    assert result == {}
    dispatcher.post.assert_awaited_once_with(
        "/accounts/{accountSlug}/invoices/123/fire.json",
        {"event": "pay"},
    )


async def test_invoices_get_model_parses_typed_view() -> None:
    dispatcher = Mock()
    dispatcher.get = AsyncMock(
        return_value=_json_response({"id": 10, "number": "2026-001", "status": "open"})
    )

    invoices = Invoices(dispatcher)
    invoice = await invoices.get_model(10)

    assert isinstance(invoice, InvoiceModel)
    assert invoice.id == 10
    assert invoice.number == "2026-001"
    assert invoice.status == InvoiceStatus.OPEN


async def test_invoices_iter_list_paginates_until_empty_page() -> None:
    dispatcher = Mock()
    dispatcher.get = AsyncMock(
        side_effect=[
            _json_response([{"id": 1}]),
            _json_response([]),
        ]
    )

    invoices = Invoices(dispatcher)
    items = [item async for item in invoices.iter_list()]

    assert items == [{"id": 1}]
    assert dispatcher.get.await_args_list == [
        call("/accounts/{accountSlug}/invoices.json", {"page": 1}),
        call("/accounts/{accountSlug}/invoices.json", {"page": 2}),
    ]
