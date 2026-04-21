from unittest.mock import AsyncMock, Mock

import httpx

from fakturoid_sdk.providers import InboxFilesProvider
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

    provider = InboxFilesProvider(dispatcher)
    response = await provider.list()

    assert response.get_body(return_json_as_dict=True) == {}
    dispatcher.get.assert_awaited_once_with("/accounts/{accountSlug}/inbox_files.json")


async def test_create() -> None:
    dispatcher = Mock()
    dispatcher.post = AsyncMock(return_value=_json_response(b'{"page": 2}'))

    provider = InboxFilesProvider(dispatcher)
    response = await provider.create({"page": 2})

    assert response.get_body(return_json_as_dict=True) == {"page": 2}
    dispatcher.post.assert_awaited_once_with(
        "/accounts/{accountSlug}/inbox_files.json",
        {"page": 2},
    )


async def test_delete() -> None:
    dispatcher = Mock()
    dispatcher.delete = AsyncMock(return_value=_json_response(b'{"page": 2}'))

    provider = InboxFilesProvider(dispatcher)
    response = await provider.delete(6)

    assert response.get_body(return_json_as_dict=True) == {"page": 2}
    dispatcher.delete.assert_awaited_once_with("/accounts/{accountSlug}/inbox_files/6.json")


async def test_send_to_ocr() -> None:
    dispatcher = Mock()
    dispatcher.post = AsyncMock(return_value=_json_response(b'{"page": 2}'))

    provider = InboxFilesProvider(dispatcher)
    response = await provider.send_to_ocr(6)

    assert response.get_body(return_json_as_dict=True) == {"page": 2}
    dispatcher.post.assert_awaited_once_with(
        "/accounts/{accountSlug}/inbox_files/6/send_to_ocr.json"
    )


async def test_download() -> None:
    dispatcher = Mock()
    dispatcher.get = AsyncMock(
        return_value=Response(
            httpx.Response(
                200,
                headers={"Content-Type": "application/pdf"},
                content=b"binary file",
            )
        )
    )

    provider = InboxFilesProvider(dispatcher)
    response = await provider.download(6)

    assert response.get_body() == "binary file"
    dispatcher.get.assert_awaited_once_with("/accounts/{accountSlug}/inbox_files/6/download")
