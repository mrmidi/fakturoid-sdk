from __future__ import annotations

from typing import Any

from fakturoid_sdk.dispatcher import Dispatcher
from fakturoid_sdk.response import Response

from .base import Provider


class SubjectsProvider(Provider):
    """Raw API provider for Subjects (Contacts) resource."""

    def __init__(self, dispatcher: Dispatcher) -> None:
        """Initializes the provider.

        Args:
            dispatcher: The dispatcher to use for API requests.
        """
        self._dispatcher = dispatcher

    async def list(self, params: dict[str, Any] | None = None) -> Response:
        """Lists subjects.

        Args:
            params: Optional query parameters (since, updated_since, page, custom_id).

        Returns:
            The raw API response.
        """
        allowed = ["since", "updated_since", "page", "custom_id"]
        return await self._dispatcher.get(
            "/accounts/{accountSlug}/subjects.json",
            self.filter_options(params, allowed),
        )

    async def search(self, params: dict[str, Any] | None = None) -> Response:
        """Searches for subjects.

        Args:
            params: Optional query parameters (query, page).

        Returns:
            The raw API response.
        """
        return await self._dispatcher.get(
            "/accounts/{accountSlug}/subjects/search.json",
            self.filter_options(params, ["query", "page"]),
        )

    async def get(self, subject_id: int) -> Response:
        """Retrieves a single subject.

        Args:
            subject_id: The identifier of the subject.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.get(f"/accounts/{{accountSlug}}/subjects/{subject_id}.json")

    async def create(self, data: dict[str, Any]) -> Response:
        """Creates a new subject.

        Args:
            data: The subject data.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.post("/accounts/{accountSlug}/subjects.json", data)

    async def update(self, subject_id: int, data: dict[str, Any]) -> Response:
        """Updates an existing subject.

        Args:
            subject_id: The identifier of the subject.
            data: The update data.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.patch(
            f"/accounts/{{accountSlug}}/subjects/{subject_id}.json",
            data,
        )

    async def delete(self, subject_id: int) -> Response:
        """Deletes a subject.

        Args:
            subject_id: The identifier of the subject.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.delete(
            f"/accounts/{{accountSlug}}/subjects/{subject_id}.json"
        )
