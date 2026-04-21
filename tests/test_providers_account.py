from unittest.mock import AsyncMock, Mock

import httpx

from fakturoid_sdk.providers import AccountProvider
from fakturoid_sdk.response import Response


async def test_get_account() -> None:
    dispatcher = Mock()
    dispatcher.get = AsyncMock(
        return_value=Response(
            httpx.Response(
                200,
                headers={"Content-Type": "application/json"},
                content=b'{"subdomain": "fakturoid-account-slug"}',
            )
        )
    )

    provider = AccountProvider(dispatcher)
    response = await provider.get()

    body = response.get_body()
    assert body.subdomain == "fakturoid-account-slug"
    assert response.get_body(return_json_as_dict=True) == {"subdomain": "fakturoid-account-slug"}

    dispatcher.get.assert_awaited_once_with("/accounts/{accountSlug}/account.json")
