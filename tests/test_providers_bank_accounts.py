from unittest.mock import AsyncMock, Mock

import httpx

from fakturoid_sdk.providers import BankAccountsProvider
from fakturoid_sdk.response import Response


async def test_list_bank_accounts() -> None:
    payload = (
        b"[{\"id\":169116,\"name\":\"Pokladna\",\"currency\":\"CZK\","
        b"\"number\":null,\"iban\":null,\"swift_bic\":null,\"pairing\":false,"
        b"\"expense_pairing\":false,\"payment_adjustment\":false,\"default\":false,"
        b"\"created_at\":\"2020-12-16T09:16:29.741+01:00\","
        b"\"updated_at\":\"2020-12-16T09:16:29.741+01:00\"}]"
    )

    dispatcher = Mock()
    dispatcher.get = AsyncMock(
        return_value=Response(
            httpx.Response(200, headers={"Content-Type": "application/json"}, content=payload)
        )
    )

    provider = BankAccountsProvider(dispatcher)
    response = await provider.list()

    body = response.get_body()
    assert body[0].id == 169116
    assert response.get_body(return_json_as_dict=True)[0]["id"] == 169116

    dispatcher.get.assert_awaited_once_with("/accounts/{accountSlug}/bank_accounts.json")
