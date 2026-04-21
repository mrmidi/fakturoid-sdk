from __future__ import annotations

from fakturoid_sdk.types import JsonValue

from .base import _Resource


class NumberFormats(_Resource):
    """Fakturoid Number Formats resource."""

    async def list(self) -> JsonValue:
        """Lists available number formats for invoices.

        Returns:
            The list of number formats as JSON.
        """
        return await self._get_json("/accounts/{accountSlug}/number_formats/invoices.json")
