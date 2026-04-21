from __future__ import annotations

from typing import Any

from fakturoid_sdk.dispatcher import Dispatcher
from fakturoid_sdk.response import Response

from .base import Provider


class TodosProvider(Provider):
    """Raw API provider for Todos resource."""

    def __init__(self, dispatcher: Dispatcher) -> None:
        """Initializes the provider.

        Args:
            dispatcher: The dispatcher to use for API requests.
        """
        self._dispatcher = dispatcher

    async def list(self, params: dict[str, Any] | None = None) -> Response:
        """Lists todos.

        Args:
            params: Optional query parameters (since, page).

        Returns:
            The raw API response.
        """
        return await self._dispatcher.get(
            "/accounts/{accountSlug}/todos.json",
            self.filter_options(params, ["since", "page"]),
        )

    async def toggle_completion(self, todo_id: int) -> Response:
        """Toggles the completion status of a todo.

        Args:
            todo_id: The identifier of the todo.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.post(
            f"/accounts/{{accountSlug}}/todos/{todo_id}/toggle_completion.json"
        )
