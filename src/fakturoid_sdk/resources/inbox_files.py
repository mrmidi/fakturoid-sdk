from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from fakturoid_sdk.types import JsonValue

from .base import _Resource


class InboxFiles(_Resource):
    """Fakturoid Inbox Files resource."""

    async def list(self) -> JsonValue:
        """Lists all files in the inbox.

        Returns:
            The list of inbox files as JSON.
        """
        return await self._get_json("/accounts/{accountSlug}/inbox_files.json")

    async def create(self, data: Mapping[str, Any]) -> JsonValue:
        """Uploads a file to the inbox.

        Args:
            data: The file data (usually contains base64 encoded content).

        Returns:
            The created inbox file as JSON.
        """
        return await self._post_json("/accounts/{accountSlug}/inbox_files.json", data)

    async def send_to_ocr(self, inbox_file_id: int) -> JsonValue:
        """Sends an inbox file to OCR processing.

        Args:
            inbox_file_id: The identifier of the inbox file.

        Returns:
            The result as JSON.
        """
        return await self._post_json(
            f"/accounts/{{accountSlug}}/inbox_files/{inbox_file_id}/send_to_ocr.json"
        )

    async def download(self, inbox_file_id: int) -> bytes:
        """Downloads an inbox file.

        Args:
            inbox_file_id: The identifier of the inbox file.

        Returns:
            The file content as bytes.
        """
        return await self._get_bytes(
            f"/accounts/{{accountSlug}}/inbox_files/{inbox_file_id}/download"
        )

    async def delete(self, inbox_file_id: int) -> JsonValue:
        """Deletes an inbox file.

        Args:
            inbox_file_id: The identifier of the inbox file.

        Returns:
            The deleted file data as JSON.
        """
        return await self._delete_json(
            f"/accounts/{{accountSlug}}/inbox_files/{inbox_file_id}.json"
        )
