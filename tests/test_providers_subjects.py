from unittest.mock import AsyncMock, Mock

import httpx
import pytest

from fakturoid_sdk.providers import SubjectsProvider
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

    provider = SubjectsProvider(dispatcher)
    response = await provider.list()

    assert response.get_body(return_json_as_dict=True) == {}
    dispatcher.get.assert_awaited_once_with("/accounts/{accountSlug}/subjects.json", {})


async def test_list_with_page() -> None:
    dispatcher = Mock()
    dispatcher.get = AsyncMock(return_value=_json_response(b'{"page": 2}'))

    provider = SubjectsProvider(dispatcher)
    response = await provider.list({"page": 2})

    assert response.get_body(return_json_as_dict=True) == {"page": 2}
    dispatcher.get.assert_awaited_once_with(
        "/accounts/{accountSlug}/subjects.json",
        {"page": 2},
    )


async def test_search() -> None:
    dispatcher = Mock()
    dispatcher.get = AsyncMock(return_value=_json_response(b'{"data": "test@fakturoid.cz"}'))

    provider = SubjectsProvider(dispatcher)
    response = await provider.search({"query": "test@fakturoid.cz", "page": 2})

    assert response.get_body(return_json_as_dict=True) == {"data": "test@fakturoid.cz"}
    dispatcher.get.assert_awaited_once_with(
        "/accounts/{accountSlug}/subjects/search.json",
        {"query": "test@fakturoid.cz", "page": 2},
    )


async def test_get() -> None:
    dispatcher = Mock()
    dispatcher.get = AsyncMock(return_value=_json_response(b'{"data": "test@fakturoid.cz"}'))

    provider = SubjectsProvider(dispatcher)
    response = await provider.get(6)

    assert response.get_body(return_json_as_dict=True) == {"data": "test@fakturoid.cz"}
    dispatcher.get.assert_awaited_once_with("/accounts/{accountSlug}/subjects/6.json")


async def test_create() -> None:
    dispatcher = Mock()
    dispatcher.post = AsyncMock(return_value=_json_response(b'{"name": "test"}'))

    provider = SubjectsProvider(dispatcher)
    response = await provider.create({"name": "test"})

    assert response.get_body(return_json_as_dict=True) == {"name": "test"}
    dispatcher.post.assert_awaited_once_with(
        "/accounts/{accountSlug}/subjects.json",
        {"name": "test"},
    )


async def test_search_with_unsupported_query_warns() -> None:
    dispatcher = Mock()
    dispatcher.get = AsyncMock(return_value=_json_response(b'{"data": "test@fakturoid.cz"}'))

    provider = SubjectsProvider(dispatcher)

    with pytest.warns(UserWarning, match=r"Unknown option keys: unknown"):
        response = await provider.search({"query": "test@fakturoid.cz", "page": 2, "unknown": "x"})

    assert response.get_body(return_json_as_dict=True) == {"data": "test@fakturoid.cz"}
    dispatcher.get.assert_awaited_once_with(
        "/accounts/{accountSlug}/subjects/search.json",
        {"query": "test@fakturoid.cz", "page": 2},
    )


async def test_update() -> None:
    dispatcher = Mock()
    dispatcher.patch = AsyncMock(return_value=_json_response(b'{"name": "test"}'))

    provider = SubjectsProvider(dispatcher)
    response = await provider.update(6, {"name": "test"})

    assert response.get_body(return_json_as_dict=True) == {"name": "test"}
    dispatcher.patch.assert_awaited_once_with(
        "/accounts/{accountSlug}/subjects/6.json",
        {"name": "test"},
    )


async def test_delete() -> None:
    dispatcher = Mock()
    dispatcher.delete = AsyncMock(return_value=_json_response(b'{"data": "test@fakturoid.cz"}'))

    provider = SubjectsProvider(dispatcher)
    response = await provider.delete(6)

    assert response.get_body(return_json_as_dict=True) == {"data": "test@fakturoid.cz"}
    dispatcher.delete.assert_awaited_once_with("/accounts/{accountSlug}/subjects/6.json")
