from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from fakturoid_sdk.types import DateLike, JsonValue

from .base import _clean_params, _Resource


class Generators(_Resource):
    """Fakturoid Generators resource."""

    async def list(
        self,
        *,
        since: DateLike | None = None,
        updated_since: DateLike | None = None,
        page: int | None = None,
        subject_id: int | None = None,
    ) -> JsonValue:
        """Lists generators.

        Args:
            since: Filter by generator date.
            updated_since: Filter by last update date.
            page: Page number for pagination.
            subject_id: Filter by subject identifier.

        Returns:
            The list of generators as JSON.
        """
        params = _clean_params(
            since=since,
            updated_since=updated_since,
            page=page,
            subject_id=subject_id,
        )
        return await self._get_json("/accounts/{accountSlug}/generators.json", params)

    async def get(self, generator_id: int) -> JsonValue:
        """Retrieves a single generator.

        Args:
            generator_id: The identifier of the generator.

        Returns:
            The generator data as JSON.
        """
        return await self._get_json(f"/accounts/{{accountSlug}}/generators/{generator_id}.json")

    async def create(self, data: Mapping[str, Any] | None = None) -> JsonValue:
        """Creates a new generator.

        Args:
            data: The generator data.

        Returns:
            The created generator as JSON.
        """
        return await self._post_json("/accounts/{accountSlug}/generators.json", data or {})

    async def update(self, generator_id: int, data: Mapping[str, Any] | None = None) -> JsonValue:
        """Updates an existing generator.

        Args:
            generator_id: The identifier of the generator.
            data: The update data.

        Returns:
            The updated generator as JSON.
        """
        return await self._patch_json(
            f"/accounts/{{accountSlug}}/generators/{generator_id}.json",
            data or {},
        )

    async def delete(self, generator_id: int) -> JsonValue:
        """Deletes a generator.

        Args:
            generator_id: The identifier of the generator.

        Returns:
            The deleted generator data as JSON.
        """
        return await self._delete_json(f"/accounts/{{accountSlug}}/generators/{generator_id}.json")
