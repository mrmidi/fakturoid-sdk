from unittest.mock import AsyncMock, Mock

import httpx

from fakturoid_sdk.providers import RecurringGeneratorsProvider
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

    provider = RecurringGeneratorsProvider(dispatcher)
    response = await provider.list({"page": 1})

    assert response.get_body(return_json_as_dict=True) == {}
    dispatcher.get.assert_awaited_once_with(
        "/accounts/{accountSlug}/recurring_generators.json",
        {"page": 1},
    )


async def test_get() -> None:
    dispatcher = Mock()
    dispatcher.get = AsyncMock(return_value=_json_response(b'{"page": 2}'))

    provider = RecurringGeneratorsProvider(dispatcher)
    response = await provider.get(6)

    assert response.get_body(return_json_as_dict=True) == {"page": 2}
    dispatcher.get.assert_awaited_once_with("/accounts/{accountSlug}/recurring_generators/6.json")


async def test_delete() -> None:
    dispatcher = Mock()
    dispatcher.delete = AsyncMock(return_value=_json_response(b'{"page": 2}'))

    provider = RecurringGeneratorsProvider(dispatcher)
    response = await provider.delete(6)

    assert response.get_body(return_json_as_dict=True) == {"page": 2}
    dispatcher.delete.assert_awaited_once_with(
        "/accounts/{accountSlug}/recurring_generators/6.json"
    )


async def test_update() -> None:
    dispatcher = Mock()
    dispatcher.patch = AsyncMock(return_value=_json_response(b'{"page": 2}'))

    provider = RecurringGeneratorsProvider(dispatcher)
    response = await provider.update(6, {"page": 2})

    assert response.get_body(return_json_as_dict=True) == {"page": 2}
    dispatcher.patch.assert_awaited_once_with(
        "/accounts/{accountSlug}/recurring_generators/6.json",
        {"page": 2},
    )


async def test_create() -> None:
    dispatcher = Mock()
    dispatcher.post = AsyncMock(return_value=_json_response(b'{"page": 2}'))

    provider = RecurringGeneratorsProvider(dispatcher)
    response = await provider.create({"page": 2})

    assert response.get_body(return_json_as_dict=True) == {"page": 2}
    dispatcher.post.assert_awaited_once_with(
        "/accounts/{accountSlug}/recurring_generators.json",
        {"page": 2},
    )


async def test_pause() -> None:
    dispatcher = Mock()
    dispatcher.patch = AsyncMock(return_value=_json_response(b'{"active": false}'))

    provider = RecurringGeneratorsProvider(dispatcher)
    response = await provider.pause(6)

    assert response.get_body(return_json_as_dict=True) == {"active": False}
    dispatcher.patch.assert_awaited_once_with(
        "/accounts/{accountSlug}/recurring_generators/6/pause.json",
        {},
    )


async def test_activate() -> None:
    dispatcher = Mock()
    dispatcher.patch = AsyncMock(return_value=_json_response(b'{"active": true}'))

    provider = RecurringGeneratorsProvider(dispatcher)
    response = await provider.activate(6)

    assert response.get_body(return_json_as_dict=True) == {"active": True}
    dispatcher.patch.assert_awaited_once_with(
        "/accounts/{accountSlug}/recurring_generators/6/activate.json",
        {},
    )


async def test_activate_with_next_occurrence_date() -> None:
    dispatcher = Mock()
    dispatcher.patch = AsyncMock(
        return_value=_json_response(b'{"active": true, "next_occurrence_on": "2025-02-15"}')
    )

    provider = RecurringGeneratorsProvider(dispatcher)
    response = await provider.activate(6, {"next_occurrence_on": "2025-02-15"})

    assert response.get_body(return_json_as_dict=True) == {
        "active": True,
        "next_occurrence_on": "2025-02-15",
    }
    dispatcher.patch.assert_awaited_once_with(
        "/accounts/{accountSlug}/recurring_generators/6/activate.json",
        {"next_occurrence_on": "2025-02-15"},
    )
