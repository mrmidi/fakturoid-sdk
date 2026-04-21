from __future__ import annotations

from typing import Any

from fakturoid_sdk.dispatcher import Dispatcher
from fakturoid_sdk.response import Response

from .base import Provider


class GeneratorsProvider(Provider):
    """Raw API provider for Generators resource."""

    def __init__(self, dispatcher: Dispatcher) -> None:
        """Initializes the provider.

        Args:
            dispatcher: The dispatcher to use for API requests.
        """
        self._dispatcher = dispatcher

    async def list(self, params: dict[str, Any] | None = None) -> Response:
        """Lists generators.

        Args:
            params: Optional query parameters (since, updated_since, page, subject_id).

        Returns:
            The raw API response.
        """
        allowed = ["since", "updated_since", "page", "subject_id"]
        return await self._dispatcher.get(
            "/accounts/{accountSlug}/generators.json",
            self.filter_options(params, allowed),
        )

    async def get(self, generator_id: int) -> Response:
        """Retrieves a single generator.

        Args:
            generator_id: The identifier of the generator.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.get(
            f"/accounts/{{accountSlug}}/generators/{generator_id}.json"
        )

    async def create(self, data: dict[str, Any] | None = None) -> Response:
        """Creates a new generator.

        Args:
            data: The generator data.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.post("/accounts/{accountSlug}/generators.json", data or {})

    async def update(self, generator_id: int, data: dict[str, Any] | None = None) -> Response:
        """Updates an existing generator.

        Args:
            generator_id: The identifier of the generator.
            data: The update data.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.patch(
            f"/accounts/{{accountSlug}}/generators/{generator_id}.json",
            data or {},
        )

    async def delete(self, generator_id: int) -> Response:
        """Deletes a generator.

        Args:
            generator_id: The identifier of the generator.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.delete(
            f"/accounts/{{accountSlug}}/generators/{generator_id}.json"
        )
