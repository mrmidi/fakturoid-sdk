from __future__ import annotations

from fakturoid_sdk.types import JsonValue

from .base import _Resource


class Users(_Resource):
    """Fakturoid Users resource."""

    async def get_current_user(self) -> JsonValue:
        """Retrieves the currently authenticated user.

        Returns:
            The user data as JSON.
        """
        return await self._get_json("/user.json")

    async def list(self) -> JsonValue:
        """Lists all users in the account.

        Returns:
            The list of users as JSON.
        """
        return await self._get_json("/accounts/{accountSlug}/users.json")
