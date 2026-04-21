from unittest.mock import AsyncMock, Mock

import httpx
import pytest

from fakturoid_sdk.providers import InvoicesProvider
from fakturoid_sdk.response import Response


def _json_response(payload: bytes) -> Response:
    return Response(
        httpx.Response(
            200,
            headers={"Content-Type": "application/json"},
            content=payload,
        )
    )


async def test_list() -> None:
    dispatcher = Mock()
    dispatcher.get = AsyncMock(return_value=_json_response(b"{}"))

    provider = InvoicesProvider(dispatcher)
    response = await provider.list({"page": 1})

    assert response.get_body(return_json_as_dict=True) == {}
    dispatcher.get.assert_awaited_once_with(
        "/accounts/{accountSlug}/invoices.json",
        {"page": 1},
    )


async def test_list_filters_and_warns_unknown_keys() -> None:
    dispatcher = Mock()
    dispatcher.get = AsyncMock(return_value=_json_response(b"{}"))

    provider = InvoicesProvider(dispatcher)
    with pytest.warns(UserWarning, match=r"Unknown option keys: unknown"):
        await provider.list({"PAGE": 1, "unknown": "x"})

    dispatcher.get.assert_awaited_once_with(
        "/accounts/{accountSlug}/invoices.json",
        {"page": 1},
    )


async def test_search() -> None:
    dispatcher = Mock()
    dispatcher.get = AsyncMock(return_value=_json_response(b'{"page": 2}'))

    provider = InvoicesProvider(dispatcher)
    response = await provider.search({"page": 2})

    assert response.get_body(return_json_as_dict=True) == {"page": 2}
    dispatcher.get.assert_awaited_once_with(
        "/accounts/{accountSlug}/invoices/search.json",
        {"page": 2},
    )


async def test_get() -> None:
    dispatcher = Mock()
    dispatcher.get = AsyncMock(return_value=_json_response(b'{"page": 2}'))

    provider = InvoicesProvider(dispatcher)
    response = await provider.get(6)

    assert response.get_body(return_json_as_dict=True) == {"page": 2}
    dispatcher.get.assert_awaited_once_with("/accounts/{accountSlug}/invoices/6.json")


async def test_get_pdf() -> None:
    dispatcher = Mock()
    dispatcher.get = AsyncMock(return_value=_json_response(b'{"page": 2}'))

    provider = InvoicesProvider(dispatcher)
    response = await provider.get_pdf(6)

    assert response.get_body(return_json_as_dict=True) == {"page": 2}
    dispatcher.get.assert_awaited_once_with("/accounts/{accountSlug}/invoices/6/download.pdf")


async def test_delete() -> None:
    dispatcher = Mock()
    dispatcher.delete = AsyncMock(return_value=_json_response(b'{"page": 2}'))

    provider = InvoicesProvider(dispatcher)
    response = await provider.delete(6)

    assert response.get_body(return_json_as_dict=True) == {"page": 2}
    dispatcher.delete.assert_awaited_once_with("/accounts/{accountSlug}/invoices/6.json")


async def test_update() -> None:
    dispatcher = Mock()
    dispatcher.patch = AsyncMock(return_value=_json_response(b'{"page": 2}'))

    provider = InvoicesProvider(dispatcher)
    response = await provider.update(6, {"page": 2})

    assert response.get_body(return_json_as_dict=True) == {"page": 2}
    dispatcher.patch.assert_awaited_once_with(
        "/accounts/{accountSlug}/invoices/6.json",
        {"page": 2},
    )


async def test_create() -> None:
    dispatcher = Mock()
    dispatcher.post = AsyncMock(return_value=_json_response(b'{"page": 2}'))

    provider = InvoicesProvider(dispatcher)
    response = await provider.create({"page": 2})

    assert response.get_body(return_json_as_dict=True) == {"page": 2}
    dispatcher.post.assert_awaited_once_with(
        "/accounts/{accountSlug}/invoices.json",
        {"page": 2},
    )


async def test_create_payment() -> None:
    dispatcher = Mock()
    dispatcher.post = AsyncMock(return_value=_json_response(b'{"page": 2}'))

    provider = InvoicesProvider(dispatcher)
    response = await provider.create_payment(6, {"page": 2})

    assert response.get_body(return_json_as_dict=True) == {"page": 2}
    dispatcher.post.assert_awaited_once_with(
        "/accounts/{accountSlug}/invoices/6/payments.json",
        {"page": 2},
    )


async def test_delete_payment() -> None:
    dispatcher = Mock()
    dispatcher.delete = AsyncMock(return_value=_json_response(b'{"page": 2}'))

    provider = InvoicesProvider(dispatcher)
    response = await provider.delete_payment(6, 8)

    assert response.get_body(return_json_as_dict=True) == {"page": 2}
    dispatcher.delete.assert_awaited_once_with("/accounts/{accountSlug}/invoices/6/payments/8.json")


async def test_get_attachment() -> None:
    dispatcher = Mock()
    dispatcher.get = AsyncMock(return_value=_json_response(b'{"page": 2}'))

    provider = InvoicesProvider(dispatcher)
    response = await provider.get_attachment(6, 8)

    assert response.get_body(return_json_as_dict=True) == {"page": 2}
    dispatcher.get.assert_awaited_once_with(
        "/accounts/{accountSlug}/invoices/6/attachments/8/download"
    )


async def test_fire_action() -> None:
    dispatcher = Mock()
    dispatcher.post = AsyncMock(return_value=_json_response(b'{"page": 2}'))

    provider = InvoicesProvider(dispatcher)
    response = await provider.fire_action(6, "pay")

    assert response.get_body(return_json_as_dict=True) == {"page": 2}
    dispatcher.post.assert_awaited_once_with(
        "/accounts/{accountSlug}/invoices/6/fire.json",
        {"event": "pay"},
    )


async def test_create_message() -> None:
    dispatcher = Mock()
    dispatcher.post = AsyncMock(return_value=_json_response(b'{"page": 2}'))

    provider = InvoicesProvider(dispatcher)
    response = await provider.create_message(
        6,
        {
            "email": "test@example.org",
            "subject": "Hello",
            "message": "Hello,\n\nI have invoice for you.\n#link#\n\n   John Doe",
        },
    )

    assert response.get_body(return_json_as_dict=True) == {"page": 2}
    dispatcher.post.assert_awaited_once_with(
        "/accounts/{accountSlug}/invoices/6/message.json",
        {
            "email": "test@example.org",
            "subject": "Hello",
            "message": "Hello,\n\nI have invoice for you.\n#link#\n\n   John Doe",
        },
    )


async def test_create_tax_document() -> None:
    dispatcher = Mock()
    dispatcher.post = AsyncMock(return_value=_json_response(b'{"page": 2}'))

    provider = InvoicesProvider(dispatcher)
    response = await provider.create_tax_document(6, 8, {"page": 2})

    assert response.get_body(return_json_as_dict=True) == {"page": 2}
    dispatcher.post.assert_awaited_once_with(
        "/accounts/{accountSlug}/invoices/6/payments/8/create_tax_document.json",
        {"page": 2},
    )
