from __future__ import annotations

from fakturoid_sdk.types import DateLike, JsonValue

from .base import _clean_params, _Resource


class Todos(_Resource):
    """Fakturoid Todos resource."""

    async def list(self, *, since: DateLike | None = None, page: int | None = None) -> JsonValue:
        """Lists todos.

        Args:
            since: Filter by date.
            page: Page number for pagination.

        Returns:
            The list of todos as JSON.
        """
        params = _clean_params(since=since, page=page)
        return await self._get_json("/accounts/{accountSlug}/todos.json", params)

    async def toggle_completion(self, todo_id: int) -> JsonValue:
        """Toggles the completion status of a todo.

        Args:
            todo_id: The identifier of the todo.

        Returns:
            The updated todo as JSON.
        """
        return await self._post_json(
            f"/accounts/{{accountSlug}}/todos/{todo_id}/toggle_completion.json"
        )
