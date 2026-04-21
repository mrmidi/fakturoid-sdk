from unittest.mock import AsyncMock, Mock

import httpx

from fakturoid_sdk.providers import NumberFormatsProvider
from fakturoid_sdk.response import Response


async def test_list_number_formats() -> None:
    payload = (
        b'[{"id":237041,"format":"F#yyyy##ddddd#",'
        b'"preview":"F202400001, F202400002, ..., F202499999",'
        b'"default":true,"created_at":"2021-01-12T15:46:03.371+01:00",'
        b'"updated_at":"2022-01-06T21:09:49.550+01:00"}]'
    )

    dispatcher = Mock()
    dispatcher.get = AsyncMock(
        return_value=Response(
            httpx.Response(200, headers={"Content-Type": "application/json"}, content=payload)
        )
    )

    provider = NumberFormatsProvider(dispatcher)
    response = await provider.list()

    body = response.get_body()
    assert body[0].id == 237041
    assert response.get_body(return_json_as_dict=True)[0]["id"] == 237041

    dispatcher.get.assert_awaited_once_with("/accounts/{accountSlug}/number_formats/invoices.json")
