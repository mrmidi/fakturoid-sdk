from __future__ import annotations

from fakturoid_sdk.types import JsonValue

from .base import _Resource


class Account(_Resource):
    """Fakturoid Account resource."""

    async def get(self) -> JsonValue:
        """Retrieves information about the current account.

        Returns:
            The account information as JSON.
        """
        return await self._get_json("/accounts/{accountSlug}/account.json")
