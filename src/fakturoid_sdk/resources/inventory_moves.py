from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from fakturoid_sdk.types import DateLike, JsonValue

from .base import _clean_params, _Resource


class InventoryMoves(_Resource):
    """Fakturoid Inventory Moves resource."""

    async def list(
        self,
        *,
        since: DateLike | None = None,
        until: DateLike | None = None,
        updated_since: DateLike | None = None,
        updated_until: DateLike | None = None,
        page: int | None = None,
        inventory_item_id: int | None = None,
    ) -> JsonValue:
        """Lists inventory moves.

        Args:
            since: Filter by date.
            until: Filter by date.
            updated_since: Filter by update date.
            updated_until: Filter by update date.
            page: Page number for pagination.
            inventory_item_id: Filter by inventory item identifier.

        Returns:
            The list of inventory moves as JSON.
        """
        params = _clean_params(
            since=since,
            until=until,
            updated_since=updated_since,
            updated_until=updated_until,
            page=page,
            inventory_item_id=inventory_item_id,
        )
        return await self._get_json("/accounts/{accountSlug}/inventory_moves.json", params)

    async def get(self, inventory_item_id: int, move_id: int) -> JsonValue:
        """Retrieves a single inventory move.

        Args:
            inventory_item_id: The identifier of the inventory item.
            move_id: The identifier of the move.

        Returns:
            The move data as JSON.
        """
        return await self._get_json(
            f"/accounts/{{accountSlug}}/inventory_items/{inventory_item_id}/inventory_moves/{move_id}.json"
        )

    async def create(self, inventory_item_id: int, data: Mapping[str, Any]) -> JsonValue:
        """Creates a new inventory move for an item.

        Args:
            inventory_item_id: The identifier of the inventory item.
            data: The move data.

        Returns:
            The created move as JSON.
        """
        return await self._post_json(
            f"/accounts/{{accountSlug}}/inventory_items/{inventory_item_id}/inventory_moves.json",
            data,
        )

    async def update(
        self,
        inventory_item_id: int,
        move_id: int,
        data: Mapping[str, Any],
    ) -> JsonValue:
        """Updates an existing inventory move.

        Args:
            inventory_item_id: The identifier of the inventory item.
            move_id: The identifier of the move.
            data: The update data.

        Returns:
            The updated move as JSON.
        """
        return await self._patch_json(
            f"/accounts/{{accountSlug}}/inventory_items/{inventory_item_id}/inventory_moves/{move_id}.json",
            data,
        )

    async def delete(self, inventory_item_id: int, move_id: int) -> JsonValue:
        """Deletes an inventory move.

        Args:
            inventory_item_id: The identifier of the inventory item.
            move_id: The identifier of the move.

        Returns:
            The deleted move data as JSON.
        """
        return await self._delete_json(
            f"/accounts/{{accountSlug}}/inventory_items/{inventory_item_id}/inventory_moves/{move_id}.json"
        )
