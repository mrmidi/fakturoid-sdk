from __future__ import annotations

from fakturoid_sdk.dispatcher import Dispatcher
from fakturoid_sdk.response import Response

from .base import Provider


class AccountProvider(Provider):
    """Raw API provider for Account resource."""

    def __init__(self, dispatcher: Dispatcher) -> None:
        """Initializes the provider.

        Args:
            dispatcher: The dispatcher to use for API requests.
        """
        self._dispatcher = dispatcher

    async def get(self) -> Response:
        """Retrieves information about the current account.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.get("/accounts/{accountSlug}/account.json")
