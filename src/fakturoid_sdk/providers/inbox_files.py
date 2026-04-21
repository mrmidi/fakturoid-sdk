from __future__ import annotations

from typing import Any

from fakturoid_sdk.dispatcher import Dispatcher
from fakturoid_sdk.response import Response

from .base import Provider


class InboxFilesProvider(Provider):
    """Raw API provider for Inbox Files resource."""

    def __init__(self, dispatcher: Dispatcher) -> None:
        """Initializes the provider.

        Args:
            dispatcher: The dispatcher to use for API requests.
        """
        self._dispatcher = dispatcher

    async def list(self) -> Response:
        """Lists all files in the inbox.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.get("/accounts/{accountSlug}/inbox_files.json")

    async def create(self, data: dict[str, Any]) -> Response:
        """Uploads a file to the inbox.

        Args:
            data: The file data (usually contains base64 encoded content).

        Returns:
            The raw API response.
        """
        return await self._dispatcher.post("/accounts/{accountSlug}/inbox_files.json", data)

    async def send_to_ocr(self, inbox_file_id: int) -> Response:
        """Sends an inbox file to OCR processing.

        Args:
            inbox_file_id: The identifier of the inbox file.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.post(
            f"/accounts/{{accountSlug}}/inbox_files/{inbox_file_id}/send_to_ocr.json"
        )

    async def download(self, inbox_file_id: int) -> Response:
        """Downloads an inbox file.

        Args:
            inbox_file_id: The identifier of the inbox file.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.get(
            f"/accounts/{{accountSlug}}/inbox_files/{inbox_file_id}/download"
        )

    async def delete(self, inbox_file_id: int) -> Response:
        """Deletes an inbox file.

        Args:
            inbox_file_id: The identifier of the inbox file.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.delete(
            f"/accounts/{{accountSlug}}/inbox_files/{inbox_file_id}.json"
        )
