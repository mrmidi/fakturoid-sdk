from unittest.mock import AsyncMock, Mock

import httpx

from fakturoid_sdk.providers import UsersProvider
from fakturoid_sdk.response import Response


async def test_get_current_user() -> None:
    dispatcher = Mock()
    dispatcher.get = AsyncMock(
        return_value=Response(
            httpx.Response(
                200,
                headers={"Content-Type": "application/json"},
                content=b'{"id": 1, "full_name": "Fakturoid"}',
            )
        )
    )

    provider = UsersProvider(dispatcher)
    response = await provider.get_current_user()

    body = response.get_body()
    assert body.id == 1
    assert body.full_name == "Fakturoid"
    assert response.get_body(return_json_as_dict=True) == {"id": 1, "full_name": "Fakturoid"}

    dispatcher.get.assert_awaited_once_with("/user.json")


async def test_list_users() -> None:
    dispatcher = Mock()
    dispatcher.get = AsyncMock(
        return_value=Response(
            httpx.Response(
                200,
                headers={"Content-Type": "application/json"},
                content=b'[{"id": 1, "full_name": "Fakturoid"}]',
            )
        )
    )

    provider = UsersProvider(dispatcher)
    response = await provider.list()

    body = response.get_body()
    assert body[0].id == 1
    assert body[0].full_name == "Fakturoid"
    assert response.get_body(return_json_as_dict=True) == [{"id": 1, "full_name": "Fakturoid"}]

    dispatcher.get.assert_awaited_once_with("/accounts/{accountSlug}/users.json")
