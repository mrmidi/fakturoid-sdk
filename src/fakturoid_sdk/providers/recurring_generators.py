from __future__ import annotations

from typing import Any

from fakturoid_sdk.dispatcher import Dispatcher
from fakturoid_sdk.response import Response

from .base import Provider


class RecurringGeneratorsProvider(Provider):
    """Raw API provider for Recurring Generators resource."""

    def __init__(self, dispatcher: Dispatcher) -> None:
        """Initializes the provider.

        Args:
            dispatcher: The dispatcher to use for API requests.
        """
        self._dispatcher = dispatcher

    async def list(self, params: dict[str, Any] | None = None) -> Response:
        """Lists recurring generators.

        Args:
            params: Optional query parameters (since, updated_since, page, subject_id).

        Returns:
            The raw API response.
        """
        allowed = ["since", "updated_since", "page", "subject_id"]
        return await self._dispatcher.get(
            "/accounts/{accountSlug}/recurring_generators.json",
            self.filter_options(params, allowed),
        )

    async def get(self, recurring_generator_id: int) -> Response:
        """Retrieves a single recurring generator.

        Args:
            recurring_generator_id: The identifier of the generator.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.get(
            f"/accounts/{{accountSlug}}/recurring_generators/{recurring_generator_id}.json"
        )

    async def create(self, data: dict[str, Any] | None = None) -> Response:
        """Creates a new recurring generator.

        Args:
            data: The generator data.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.post(
            "/accounts/{accountSlug}/recurring_generators.json",
            data or {},
        )

    async def update(
        self,
        recurring_generator_id: int,
        data: dict[str, Any] | None = None,
    ) -> Response:
        """Updates an existing recurring generator.

        Args:
            recurring_generator_id: The identifier of the generator.
            data: The update data.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.patch(
            f"/accounts/{{accountSlug}}/recurring_generators/{recurring_generator_id}.json",
            data or {},
        )

    async def delete(self, recurring_generator_id: int) -> Response:
        """Deletes a recurring generator.

        Args:
            recurring_generator_id: The identifier of the generator.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.delete(
            f"/accounts/{{accountSlug}}/recurring_generators/{recurring_generator_id}.json"
        )

    async def pause(self, recurring_generator_id: int) -> Response:
        """Pauses a recurring generator.

        Args:
            recurring_generator_id: The identifier of the generator.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.patch(
            f"/accounts/{{accountSlug}}/recurring_generators/{recurring_generator_id}/pause.json",
            {},
        )

    async def activate(
        self,
        recurring_generator_id: int,
        data: dict[str, Any] | None = None,
    ) -> Response:
        """Activates a paused recurring generator.

        Args:
            recurring_generator_id: The identifier of the generator.
            data: Optional activation data.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.patch(
            f"/accounts/{{accountSlug}}/recurring_generators/{recurring_generator_id}/activate.json",
            data or {},
        )
