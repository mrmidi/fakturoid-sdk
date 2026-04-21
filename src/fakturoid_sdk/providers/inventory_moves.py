from __future__ import annotations

from typing import Any

from fakturoid_sdk.dispatcher import Dispatcher
from fakturoid_sdk.response import Response

from .base import Provider


class InventoryMovesProvider(Provider):
    """Raw API provider for Inventory Moves resource."""

    def __init__(self, dispatcher: Dispatcher) -> None:
        """Initializes the provider.

        Args:
            dispatcher: The dispatcher to use for API requests.
        """
        self._dispatcher = dispatcher

    async def list(self, params: dict[str, Any] | None = None) -> Response:
        """Lists inventory moves.

        Args:
            params: Optional query parameters (since, until, updated_since,
                updated_until, page, inventory_item_id).

        Returns:
            The raw API response.
        """
        allowed = [
            "since",
            "until",
            "updated_since",
            "updated_until",
            "page",
            "inventory_item_id",
        ]
        return await self._dispatcher.get(
            "/accounts/{accountSlug}/inventory_moves.json",
            self.filter_options(params, allowed),
        )

    async def get(self, inventory_item_id: int, move_id: int) -> Response:
        """Retrieves a single inventory move.

        Args:
            inventory_item_id: The identifier of the inventory item.
            move_id: The identifier of the move.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.get(
            f"/accounts/{{accountSlug}}/inventory_items/{inventory_item_id}/inventory_moves/{move_id}.json"
        )

    async def create(self, inventory_item_id: int, data: dict[str, Any]) -> Response:
        """Creates a new inventory move for an item.

        Args:
            inventory_item_id: The identifier of the inventory item.
            data: The move data.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.post(
            f"/accounts/{{accountSlug}}/inventory_items/{inventory_item_id}/inventory_moves.json",
            data,
        )

    async def update(self, inventory_item_id: int, move_id: int, data: dict[str, Any]) -> Response:
        """Updates an existing inventory move.

        Args:
            inventory_item_id: The identifier of the inventory item.
            move_id: The identifier of the move.
            data: The update data.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.patch(
            f"/accounts/{{accountSlug}}/inventory_items/{inventory_item_id}/inventory_moves/{move_id}.json",
            data,
        )

    async def delete(self, inventory_item_id: int, move_id: int) -> Response:
        """Deletes an inventory move.

        Args:
            inventory_item_id: The identifier of the inventory item.
            move_id: The identifier of the move.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.delete(
            f"/accounts/{{accountSlug}}/inventory_items/{inventory_item_id}/inventory_moves/{move_id}.json"
        )
