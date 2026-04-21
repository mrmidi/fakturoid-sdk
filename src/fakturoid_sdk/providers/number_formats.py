from __future__ import annotations

from fakturoid_sdk.dispatcher import Dispatcher
from fakturoid_sdk.response import Response

from .base import Provider


class NumberFormatsProvider(Provider):
    """Raw API provider for Number Formats resource."""

    def __init__(self, dispatcher: Dispatcher) -> None:
        """Initializes the provider.

        Args:
            dispatcher: The dispatcher to use for API requests.
        """
        self._dispatcher = dispatcher

    async def list(self) -> Response:
        """Lists available number formats for invoices.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.get("/accounts/{accountSlug}/number_formats/invoices.json")
