from __future__ import annotations

from typing import Any

from fakturoid_sdk.dispatcher import Dispatcher
from fakturoid_sdk.response import Response

from .base import Provider


class InventoryItemsProvider(Provider):
    """Raw API provider for Inventory Items resource."""

    def __init__(self, dispatcher: Dispatcher) -> None:
        """Initializes the provider.

        Args:
            dispatcher: The dispatcher to use for API requests.
        """
        self._dispatcher = dispatcher

    async def list(self, params: dict[str, Any] | None = None) -> Response:
        """Lists inventory items.

        Args:
            params: Optional query parameters (since, until, updated_since,
                updated_until, page, article_number, sku).

        Returns:
            The raw API response.
        """
        allowed = [
            "since",
            "until",
            "updated_since",
            "updated_until",
            "page",
            "article_number",
            "sku",
        ]
        return await self._dispatcher.get(
            "/accounts/{accountSlug}/inventory_items.json",
            self.filter_options(params, allowed),
        )

    async def list_archived(self, params: dict[str, Any] | None = None) -> Response:
        """Lists archived inventory items.

        Args:
            params: Optional query parameters (since, until, updated_since,
                updated_until, page, article_number, sku).

        Returns:
            The raw API response.
        """
        allowed = [
            "since",
            "until",
            "updated_since",
            "updated_until",
            "page",
            "article_number",
            "sku",
        ]
        return await self._dispatcher.get(
            "/accounts/{accountSlug}/inventory_items/archived.json",
            self.filter_options(params, allowed),
        )

    async def list_low_quantity(self, params: dict[str, Any] | None = None) -> Response:
        """Lists inventory items with low quantity.

        Args:
            params: Optional query parameters (page).

        Returns:
            The raw API response.
        """
        return await self._dispatcher.get(
            "/accounts/{accountSlug}/inventory_items/low_quantity.json",
            self.filter_options(params, ["page"]),
        )

    async def search(self, params: dict[str, Any] | None = None) -> Response:
        """Searches for inventory items.

        Args:
            params: Optional query parameters (query, page).

        Returns:
            The raw API response.
        """
        return await self._dispatcher.get(
            "/accounts/{accountSlug}/inventory_items/search.json",
            self.filter_options(params, ["query", "page"]),
        )

    async def get(self, item_id: int) -> Response:
        """Retrieves a single inventory item.

        Args:
            item_id: The identifier of the item.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.get(
            f"/accounts/{{accountSlug}}/inventory_items/{item_id}.json"
        )

    async def create(self, data: dict[str, Any]) -> Response:
        """Creates a new inventory item.

        Args:
            data: The item data.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.post("/accounts/{accountSlug}/inventory_items.json", data)

    async def update(self, item_id: int, data: dict[str, Any]) -> Response:
        """Updates an existing inventory item.

        Args:
            item_id: The identifier of the item.
            data: The update data.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.patch(
            f"/accounts/{{accountSlug}}/inventory_items/{item_id}.json",
            data,
        )

    async def delete(self, item_id: int) -> Response:
        """Deletes an inventory item.

        Args:
            item_id: The identifier of the item.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.delete(
            f"/accounts/{{accountSlug}}/inventory_items/{item_id}.json"
        )

    async def archive(self, item_id: int) -> Response:
        """Archives an inventory item.

        Args:
            item_id: The identifier of the item.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.post(
            f"/accounts/{{accountSlug}}/inventory_items/{item_id}/archive.json"
        )

    async def unarchive(self, item_id: int) -> Response:
        """Unarchives an inventory item.

        Args:
            item_id: The identifier of the item.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.post(
            f"/accounts/{{accountSlug}}/inventory_items/{item_id}/unarchive.json"
        )
