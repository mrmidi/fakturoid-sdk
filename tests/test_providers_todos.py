from unittest.mock import AsyncMock, Mock

import httpx

from fakturoid_sdk.providers import TodosProvider
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

    provider = TodosProvider(dispatcher)
    response = await provider.list()

    assert response.get_body(return_json_as_dict=True) == {}
    dispatcher.get.assert_awaited_once_with("/accounts/{accountSlug}/todos.json", {})


async def test_list_with_page() -> None:
    dispatcher = Mock()
    dispatcher.get = AsyncMock(return_value=_json_response(b'{"page": 2}'))

    provider = TodosProvider(dispatcher)
    response = await provider.list({"page": 2})

    assert response.get_body(return_json_as_dict=True) == {"page": 2}
    dispatcher.get.assert_awaited_once_with(
        "/accounts/{accountSlug}/todos.json",
        {"page": 2},
    )


async def test_toggle_completion() -> None:
    dispatcher = Mock()
    dispatcher.post = AsyncMock(return_value=_json_response(b"{}"))

    provider = TodosProvider(dispatcher)
    response = await provider.toggle_completion(6)

    assert response.get_body(return_json_as_dict=True) == {}
    dispatcher.post.assert_awaited_once_with(
        "/accounts/{accountSlug}/todos/6/toggle_completion.json"
    )
