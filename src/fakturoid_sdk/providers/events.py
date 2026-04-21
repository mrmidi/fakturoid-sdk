from __future__ import annotations

from typing import Any

from fakturoid_sdk.dispatcher import Dispatcher
from fakturoid_sdk.response import Response

from .base import Provider


class EventsProvider(Provider):
    """Raw API provider for Events resource."""

    def __init__(self, dispatcher: Dispatcher) -> None:
        """Initializes the provider.

        Args:
            dispatcher: The dispatcher to use for API requests.
        """
        self._dispatcher = dispatcher

    async def list(self, params: dict[str, Any] | None = None) -> Response:
        """Lists all events.

        Args:
            params: Optional query parameters (subject_id, since, page).

        Returns:
            The raw API response.
        """
        return await self._dispatcher.get(
            "/accounts/{accountSlug}/events.json",
            self.filter_options(params, ["subject_id", "since", "page"]),
        )

    async def list_paid(self, params: dict[str, Any] | None = None) -> Response:
        """Lists only 'paid' events.

        Args:
            params: Optional query parameters (subject_id, since, page).

        Returns:
            The raw API response.
        """
        return await self._dispatcher.get(
            "/accounts/{accountSlug}/events/paid.json",
            self.filter_options(params, ["subject_id", "since", "page"]),
        )
