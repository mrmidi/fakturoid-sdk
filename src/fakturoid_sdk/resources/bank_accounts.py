from __future__ import annotations

from fakturoid_sdk.types import JsonValue

from .base import _Resource


class BankAccounts(_Resource):
    """Fakturoid Bank Accounts resource."""

    async def list(self) -> JsonValue:
        """Lists all bank accounts.

        Returns:
            The list of bank accounts as JSON.
        """
        return await self._get_json("/accounts/{accountSlug}/bank_accounts.json")
