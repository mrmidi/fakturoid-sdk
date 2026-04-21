from __future__ import annotations

from typing import Any

from fakturoid_sdk.dispatcher import Dispatcher
from fakturoid_sdk.response import Response

from .base import Provider


class WebhooksProvider(Provider):
    """Raw API provider for Webhooks resource."""

    def __init__(self, dispatcher: Dispatcher) -> None:
        """Initializes the provider.

        Args:
            dispatcher: The dispatcher to use for API requests.
        """
        self._dispatcher = dispatcher

    async def list(self, params: dict[str, Any] | None = None) -> Response:
        """Lists webhooks.

        Args:
            params: Optional query parameters (page).

        Returns:
            The raw API response.
        """
        return await self._dispatcher.get(
            "/accounts/{accountSlug}/webhooks.json",
            self.filter_options(params, ["page"]),
        )

    async def get(self, webhook_id: int) -> Response:
        """Retrieves a single webhook.

        Args:
            webhook_id: The identifier of the webhook.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.get(
            f"/accounts/{{accountSlug}}/webhooks/{webhook_id}.json"
        )

    async def create(self, data: dict[str, Any]) -> Response:
        """Creates a new webhook.

        Args:
            data: The webhook data (URL, events).

        Returns:
            The raw API response.
        """
        return await self._dispatcher.post("/accounts/{accountSlug}/webhooks.json", data)

    async def update(self, webhook_id: int, data: dict[str, Any]) -> Response:
        """Updates an existing webhook.

        Args:
            webhook_id: The identifier of the webhook.
            data: The update data.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.patch(
            f"/accounts/{{accountSlug}}/webhooks/{webhook_id}.json",
            data,
        )

    async def delete(self, webhook_id: int) -> Response:
        """Deletes a webhook.

        Args:
            webhook_id: The identifier of the webhook.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.delete(
            f"/accounts/{{accountSlug}}/webhooks/{webhook_id}.json"
        )
