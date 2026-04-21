from __future__ import annotations

from fakturoid_sdk.dispatcher import Dispatcher
from fakturoid_sdk.response import Response

from .base import Provider


class UsersProvider(Provider):
    """Raw API provider for Users resource."""

    def __init__(self, dispatcher: Dispatcher) -> None:
        """Initializes the provider.

        Args:
            dispatcher: The dispatcher to use for API requests.
        """
        self._dispatcher = dispatcher

    async def get_current_user(self) -> Response:
        """Retrieves the currently authenticated user.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.get("/user.json")

    async def list(self) -> Response:
        """Lists all users in the account.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.get("/accounts/{accountSlug}/users.json")
