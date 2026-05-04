from __future__ import annotations

from typing import Any

from fakturoid_sdk.dispatcher import Dispatcher
from fakturoid_sdk.response import Response

from .base import Provider


class ExpensesProvider(Provider):
    """Raw API provider for Expenses resource."""

    def __init__(self, dispatcher: Dispatcher) -> None:
        """Initializes the provider.

        Args:
            dispatcher: The dispatcher to use for API requests.
        """
        self._dispatcher = dispatcher

    async def list(self, params: dict[str, Any] | None = None) -> Response:
        """Lists expenses.

        Args:
            params: Optional query parameters (since, updated_since, page, subject_id,
                custom_id, number, variable_symbol, status, document_type).

        Returns:
            The raw API response.
        """
        allowed = [
            "since",
            "updated_since",
            "page",
            "subject_id",
            "custom_id",
            "number",
            "variable_symbol",
            "status",
            "document_type",
        ]
        return await self._dispatcher.get(
            "/accounts/{accountSlug}/expenses.json",
            self.filter_options(params, allowed),
        )

    async def search(self, params: dict[str, Any] | None = None) -> Response:
        """Searches for expenses.

        Args:
            params: Optional query parameters (query, page, tags).

        Returns:
            The raw API response.
        """
        return await self._dispatcher.get(
            "/accounts/{accountSlug}/expenses/search.json",
            self.filter_options(params, ["query", "page", "tags"]),
        )

    async def get(self, expense_id: int) -> Response:
        """Retrieves a single expense.

        Args:
            expense_id: The identifier of the expense.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.get(f"/accounts/{{accountSlug}}/expenses/{expense_id}.json")

    async def get_attachment(self, expense_id: int, attachment_id: int) -> Response:
        """Downloads an expense attachment.

        Args:
            expense_id: The identifier of the expense.
            attachment_id: The identifier of the attachment.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.get(
            f"/accounts/{{accountSlug}}/expenses/{expense_id}/attachments/{attachment_id}/download"
        )

    async def fire_action(self, expense_id: int, event: str) -> Response:
        """Fires a workflow event on an expense.

        Args:
            expense_id: The identifier of the expense.
            event: The action event to fire.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.post(
            f"/accounts/{{accountSlug}}/expenses/{expense_id}/fire.json",
            query_params={"event": event},
        )

    async def create(self, data: dict[str, Any]) -> Response:
        """Creates a new expense.

        Args:
            data: The expense data.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.post("/accounts/{accountSlug}/expenses.json", data)

    async def update(self, expense_id: int, data: dict[str, Any]) -> Response:
        """Updates an existing expense.

        Args:
            expense_id: The identifier of the expense.
            data: The update data.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.patch(
            f"/accounts/{{accountSlug}}/expenses/{expense_id}.json",
            data,
        )

    async def delete(self, expense_id: int) -> Response:
        """Deletes an expense.

        Args:
            expense_id: The identifier of the expense.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.delete(
            f"/accounts/{{accountSlug}}/expenses/{expense_id}.json"
        )

    async def create_payment(self, expense_id: int, data: dict[str, Any] | None = None) -> Response:
        """Records a payment for an expense.

        Args:
            expense_id: The identifier of the expense.
            data: Optional payment data.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.post(
            f"/accounts/{{accountSlug}}/expenses/{expense_id}/payments.json",
            data or {},
        )

    async def delete_payment(self, expense_id: int, payment_id: int) -> Response:
        """Deletes an expense payment.

        Args:
            expense_id: The identifier of the expense.
            payment_id: The identifier of the payment.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.delete(
            f"/accounts/{{accountSlug}}/expenses/{expense_id}/payments/{payment_id}.json"
        )
