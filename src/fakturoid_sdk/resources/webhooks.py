from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from fakturoid_sdk.types import JsonValue

from .base import _clean_params, _Resource


class Webhooks(_Resource):
    """Fakturoid Webhooks resource."""

    async def list(self, *, page: int | None = None) -> JsonValue:
        """Lists webhooks.

        Args:
            page: Page number for pagination.

        Returns:
            The list of webhooks as JSON.
        """
        params = _clean_params(page=page)
        return await self._get_json("/accounts/{accountSlug}/webhooks.json", params)

    async def get(self, webhook_id: int) -> JsonValue:
        """Retrieves a single webhook.

        Args:
            webhook_id: The identifier of the webhook.

        Returns:
            The webhook data as JSON.
        """
        return await self._get_json(f"/accounts/{{accountSlug}}/webhooks/{webhook_id}.json")

    async def create(self, data: Mapping[str, Any]) -> JsonValue:
        """Creates a new webhook.

        Args:
            data: The webhook data (URL, events).

        Returns:
            The created webhook as JSON.
        """
        return await self._post_json("/accounts/{accountSlug}/webhooks.json", data)

    async def update(self, webhook_id: int, data: Mapping[str, Any]) -> JsonValue:
        """Updates an existing webhook.

        Args:
            webhook_id: The identifier of the webhook.
            data: The update data.

        Returns:
            The updated webhook as JSON.
        """
        return await self._patch_json(
            f"/accounts/{{accountSlug}}/webhooks/{webhook_id}.json",
            data,
        )

    async def delete(self, webhook_id: int) -> JsonValue:
        """Deletes a webhook.

        Args:
            webhook_id: The identifier of the webhook.

        Returns:
            The deleted webhook data as JSON.
        """
        return await self._delete_json(f"/accounts/{{accountSlug}}/webhooks/{webhook_id}.json")
