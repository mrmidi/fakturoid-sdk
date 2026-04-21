from unittest.mock import AsyncMock, Mock

import httpx

from fakturoid_sdk.providers import InventoryMovesProvider
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

    provider = InventoryMovesProvider(dispatcher)
    response = await provider.list({"page": 1})

    assert response.get_body(return_json_as_dict=True) == {}
    dispatcher.get.assert_awaited_once_with(
        "/accounts/{accountSlug}/inventory_moves.json",
        {"page": 1},
    )


async def test_get() -> None:
    dispatcher = Mock()
    dispatcher.get = AsyncMock(return_value=_json_response(b"{}"))

    provider = InventoryMovesProvider(dispatcher)
    response = await provider.get(8, 60)

    assert response.get_body(return_json_as_dict=True) == {}
    dispatcher.get.assert_awaited_once_with(
        "/accounts/{accountSlug}/inventory_items/8/inventory_moves/60.json"
    )


async def test_delete() -> None:
    dispatcher = Mock()
    dispatcher.delete = AsyncMock(return_value=_json_response(b'{"page": 2}'))

    provider = InventoryMovesProvider(dispatcher)
    response = await provider.delete(8, 60)

    assert response.get_body(return_json_as_dict=True) == {"page": 2}
    dispatcher.delete.assert_awaited_once_with(
        "/accounts/{accountSlug}/inventory_items/8/inventory_moves/60.json"
    )


async def test_update() -> None:
    dispatcher = Mock()
    dispatcher.patch = AsyncMock(return_value=_json_response(b'{"page": 2}'))

    provider = InventoryMovesProvider(dispatcher)
    response = await provider.update(8, 60, {"page": 2})

    assert response.get_body(return_json_as_dict=True) == {"page": 2}
    dispatcher.patch.assert_awaited_once_with(
        "/accounts/{accountSlug}/inventory_items/8/inventory_moves/60.json",
        {"page": 2},
    )


async def test_create() -> None:
    dispatcher = Mock()
    dispatcher.post = AsyncMock(return_value=_json_response(b'{"page": 2}'))

    provider = InventoryMovesProvider(dispatcher)
    response = await provider.create(8, {"page": 2})

    assert response.get_body(return_json_as_dict=True) == {"page": 2}
    dispatcher.post.assert_awaited_once_with(
        "/accounts/{accountSlug}/inventory_items/8/inventory_moves.json",
        {"page": 2},
    )
