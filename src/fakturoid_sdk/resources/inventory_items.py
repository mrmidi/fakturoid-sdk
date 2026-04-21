from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from fakturoid_sdk.types import DateLike, JsonValue

from .base import _clean_params, _Resource


class InventoryItems(_Resource):
    """Fakturoid Inventory Items resource."""

    async def list(
        self,
        *,
        since: DateLike | None = None,
        until: DateLike | None = None,
        updated_since: DateLike | None = None,
        updated_until: DateLike | None = None,
        page: int | None = None,
        article_number: str | None = None,
        sku: str | None = None,
    ) -> JsonValue:
        """Lists inventory items.

        Args:
            since: Filter by date.
            until: Filter by date.
            updated_since: Filter by update date.
            updated_until: Filter by update date.
            page: Page number for pagination.
            article_number: Filter by article number.
            sku: Filter by SKU.

        Returns:
            The list of inventory items as JSON.
        """
        params = _clean_params(
            since=since,
            until=until,
            updated_since=updated_since,
            updated_until=updated_until,
            page=page,
            article_number=article_number,
            sku=sku,
        )
        return await self._get_json("/accounts/{accountSlug}/inventory_items.json", params)

    async def list_archived(
        self,
        *,
        since: DateLike | None = None,
        until: DateLike | None = None,
        updated_since: DateLike | None = None,
        updated_until: DateLike | None = None,
        page: int | None = None,
        article_number: str | None = None,
        sku: str | None = None,
    ) -> JsonValue:
        """Lists archived inventory items.

        Args:
            since: Filter by date.
            until: Filter by date.
            updated_since: Filter by update date.
            updated_until: Filter by update date.
            page: Page number for pagination.
            article_number: Filter by article number.
            sku: Filter by SKU.

        Returns:
            The list of archived inventory items as JSON.
        """
        params = _clean_params(
            since=since,
            until=until,
            updated_since=updated_since,
            updated_until=updated_until,
            page=page,
            article_number=article_number,
            sku=sku,
        )
        return await self._get_json(
            "/accounts/{accountSlug}/inventory_items/archived.json",
            params,
        )

    async def list_low_quantity(self, *, page: int | None = None) -> JsonValue:
        """Lists inventory items with low quantity.

        Args:
            page: Page number for pagination.

        Returns:
            The list of items as JSON.
        """
        params = _clean_params(page=page)
        return await self._get_json(
            "/accounts/{accountSlug}/inventory_items/low_quantity.json",
            params,
        )

    async def search(self, *, query: str, page: int | None = None) -> JsonValue:
        """Searches for inventory items.

        Args:
            query: Search query string.
            page: Page number for pagination.

        Returns:
            The search results as JSON.
        """
        params = _clean_params(query=query, page=page)
        return await self._get_json("/accounts/{accountSlug}/inventory_items/search.json", params)

    async def get(self, item_id: int) -> JsonValue:
        """Retrieves a single inventory item.

        Args:
            item_id: The identifier of the item.

        Returns:
            The item data as JSON.
        """
        return await self._get_json(f"/accounts/{{accountSlug}}/inventory_items/{item_id}.json")

    async def create(self, data: Mapping[str, Any]) -> JsonValue:
        """Creates a new inventory item.

        Args:
            data: The item data.

        Returns:
            The created item as JSON.
        """
        return await self._post_json("/accounts/{accountSlug}/inventory_items.json", data)

    async def update(self, item_id: int, data: Mapping[str, Any]) -> JsonValue:
        """Updates an existing inventory item.

        Args:
            item_id: The identifier of the item.
            data: The update data.

        Returns:
            The updated item as JSON.
        """
        return await self._patch_json(
            f"/accounts/{{accountSlug}}/inventory_items/{item_id}.json",
            data,
        )

    async def delete(self, item_id: int) -> JsonValue:
        """Deletes an inventory item.

        Args:
            item_id: The identifier of the item.

        Returns:
            The deleted item data as JSON.
        """
        return await self._delete_json(f"/accounts/{{accountSlug}}/inventory_items/{item_id}.json")

    async def archive(self, item_id: int) -> JsonValue:
        """Archives an inventory item.

        Args:
            item_id: The identifier of the item.

        Returns:
            The archived item data as JSON.
        """
        return await self._post_json(
            f"/accounts/{{accountSlug}}/inventory_items/{item_id}/archive.json"
        )

    async def unarchive(self, item_id: int) -> JsonValue:
        """Unarchives an inventory item.

        Args:
            item_id: The identifier of the item.

        Returns:
            The unarchived item data as JSON.
        """
        return await self._post_json(
            f"/accounts/{{accountSlug}}/inventory_items/{item_id}/unarchive.json"
        )
