from unittest.mock import AsyncMock, Mock

import httpx

from fakturoid_sdk.providers import EventsProvider
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

    provider = EventsProvider(dispatcher)
    response = await provider.list()

    assert response.get_body(return_json_as_dict=True) == {}
    dispatcher.get.assert_awaited_once_with("/accounts/{accountSlug}/events.json", {})


async def test_list_paid() -> None:
    dispatcher = Mock()
    dispatcher.get = AsyncMock(return_value=_json_response(b'{"page": 2}'))

    provider = EventsProvider(dispatcher)
    response = await provider.list_paid({"page": 2})

    assert response.get_body(return_json_as_dict=True) == {"page": 2}
    dispatcher.get.assert_awaited_once_with(
        "/accounts/{accountSlug}/events/paid.json",
        {"page": 2},
    )
