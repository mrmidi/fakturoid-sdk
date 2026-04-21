from unittest.mock import AsyncMock, Mock

import httpx

from fakturoid_sdk.providers import InventoryItemsProvider
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

    provider = InventoryItemsProvider(dispatcher)
    response = await provider.list({"page": 1})

    assert response.get_body(return_json_as_dict=True) == {}
    dispatcher.get.assert_awaited_once_with(
        "/accounts/{accountSlug}/inventory_items.json",
        {"page": 1},
    )


async def test_list_archived() -> None:
    dispatcher = Mock()
    dispatcher.get = AsyncMock(return_value=_json_response(b"{}"))

    provider = InventoryItemsProvider(dispatcher)
    response = await provider.list_archived({"page": 1})

    assert response.get_body(return_json_as_dict=True) == {}
    dispatcher.get.assert_awaited_once_with(
        "/accounts/{accountSlug}/inventory_items/archived.json",
        {"page": 1},
    )


async def test_list_low_quantity() -> None:
    dispatcher = Mock()
    dispatcher.get = AsyncMock(return_value=_json_response(b"{}"))

    provider = InventoryItemsProvider(dispatcher)
    response = await provider.list_low_quantity({"page": 1})

    assert response.get_body(return_json_as_dict=True) == {}
    dispatcher.get.assert_awaited_once_with(
        "/accounts/{accountSlug}/inventory_items/low_quantity.json",
        {"page": 1},
    )


async def test_search() -> None:
    dispatcher = Mock()
    dispatcher.get = AsyncMock(return_value=_json_response(b'{"page": 2}'))

    provider = InventoryItemsProvider(dispatcher)
    response = await provider.search({"page": 2})

    assert response.get_body(return_json_as_dict=True) == {"page": 2}
    dispatcher.get.assert_awaited_once_with(
        "/accounts/{accountSlug}/inventory_items/search.json",
        {"page": 2},
    )


async def test_get() -> None:
    dispatcher = Mock()
    dispatcher.get = AsyncMock(return_value=_json_response(b'{"page": 2}'))

    provider = InventoryItemsProvider(dispatcher)
    response = await provider.get(6)

    assert response.get_body(return_json_as_dict=True) == {"page": 2}
    dispatcher.get.assert_awaited_once_with("/accounts/{accountSlug}/inventory_items/6.json")


async def test_delete() -> None:
    dispatcher = Mock()
    dispatcher.delete = AsyncMock(return_value=_json_response(b'{"page": 2}'))

    provider = InventoryItemsProvider(dispatcher)
    response = await provider.delete(6)

    assert response.get_body(return_json_as_dict=True) == {"page": 2}
    dispatcher.delete.assert_awaited_once_with("/accounts/{accountSlug}/inventory_items/6.json")


async def test_update() -> None:
    dispatcher = Mock()
    dispatcher.patch = AsyncMock(return_value=_json_response(b'{"page": 2}'))

    provider = InventoryItemsProvider(dispatcher)
    response = await provider.update(6, {"page": 2})

    assert response.get_body(return_json_as_dict=True) == {"page": 2}
    dispatcher.patch.assert_awaited_once_with(
        "/accounts/{accountSlug}/inventory_items/6.json",
        {"page": 2},
    )


async def test_create() -> None:
    dispatcher = Mock()
    dispatcher.post = AsyncMock(return_value=_json_response(b'{"page": 2}'))

    provider = InventoryItemsProvider(dispatcher)
    response = await provider.create({"page": 2})

    assert response.get_body(return_json_as_dict=True) == {"page": 2}
    dispatcher.post.assert_awaited_once_with(
        "/accounts/{accountSlug}/inventory_items.json",
        {"page": 2},
    )


async def test_archive() -> None:
    dispatcher = Mock()
    dispatcher.post = AsyncMock(return_value=_json_response(b'{"page": 2}'))

    provider = InventoryItemsProvider(dispatcher)
    response = await provider.archive(6)

    assert response.get_body(return_json_as_dict=True) == {"page": 2}
    dispatcher.post.assert_awaited_once_with(
        "/accounts/{accountSlug}/inventory_items/6/archive.json"
    )


async def test_unarchive() -> None:
    dispatcher = Mock()
    dispatcher.post = AsyncMock(return_value=_json_response(b'{"page": 2}'))

    provider = InventoryItemsProvider(dispatcher)
    response = await provider.unarchive(6)

    assert response.get_body(return_json_as_dict=True) == {"page": 2}
    dispatcher.post.assert_awaited_once_with(
        "/accounts/{accountSlug}/inventory_items/6/unarchive.json"
    )
