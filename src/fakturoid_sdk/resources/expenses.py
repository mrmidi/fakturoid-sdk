from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from fakturoid_sdk.enums import ExpenseEvent, ExpenseStatus
from fakturoid_sdk.models import Expense as ExpenseModel
from fakturoid_sdk.types import DateLike, JsonValue

from .base import _clean_params, _parse_model, _Resource


class Expenses(_Resource):
    """Fakturoid Expenses resource."""

    async def list(
        self,
        *,
        since: DateLike | None = None,
        updated_since: DateLike | None = None,
        page: int | None = None,
        subject_id: int | None = None,
        custom_id: str | None = None,
        number: str | None = None,
        variable_symbol: str | None = None,
        status: str | ExpenseStatus | None = None,
        document_type: str | None = None,
    ) -> JsonValue:
        """Lists expenses.

        See: https://www.fakturoid.cz/api/v3/expenses#get-accounts-slug-expenses-json

        Args:
            since: Filter by expense date.
            updated_since: Filter by last update date.
            page: Page number for pagination.
            subject_id: Filter by subject identifier.
            custom_id: Filter by custom identifier.
            number: Filter by expense number.
            variable_symbol: Filter by variable symbol.
            status: Filter by expense status.
            document_type: Filter by document type (invoice, bill, other).

        Returns:
            The list of expenses as JSON.
        """
        params = _clean_params(
            since=since,
            updated_since=updated_since,
            page=page,
            subject_id=subject_id,
            custom_id=custom_id,
            number=number,
            variable_symbol=variable_symbol,
            status=status,
            document_type=document_type,
        )
        return await self._get_json("/accounts/{accountSlug}/expenses.json", params)

    async def search(
        self,
        *,
        query: str,
        page: int | None = None,
        tags: str | Sequence[str] | None = None,
    ) -> JsonValue:
        """Searches for expenses.

        Args:
            query: Search query string.
            page: Page number for pagination.
            tags: Filter by tags.

        Returns:
            The search results as JSON.
        """
        params = _clean_params(query=query, page=page, tags=tags)
        return await self._get_json("/accounts/{accountSlug}/expenses/search.json", params)

    async def get(self, expense_id: int) -> JsonValue:
        """Retrieves a single expense.

        See: https://www.fakturoid.cz/api/v3/expenses#get-accounts-slug-expenses-id-json

        Args:
            expense_id: The identifier of the expense.

        Returns:
            The expense data as JSON.
        """
        return await self._get_json(f"/accounts/{{accountSlug}}/expenses/{expense_id}.json")

    async def get_attachment(self, expense_id: int, attachment_id: int) -> bytes:
        """Downloads an expense attachment.

        Args:
            expense_id: The identifier of the expense.
            attachment_id: The identifier of the attachment.

        Returns:
            The attachment content as bytes.
        """
        return await self._get_bytes(
            f"/accounts/{{accountSlug}}/expenses/{expense_id}/attachments/{attachment_id}/download"
        )

    async def fire_action(self, expense_id: int, *, event: str) -> JsonValue:
        """Fires a workflow event on an expense.

        See: https://www.fakturoid.cz/api/v3/expenses#post-accounts-slug-expenses-id-fire-json

        Args:
            expense_id: The identifier of the expense.
            event: The action event to fire.

        Returns:
            The result of the action as JSON.
        """
        return await self._post_json(
            f"/accounts/{{accountSlug}}/expenses/{expense_id}/fire.json",
            params={"event": event},
        )

    async def fire(self, expense_id: int, *, event: ExpenseEvent) -> JsonValue:
        """Fires a typed workflow event on an expense.

        Args:
            expense_id: The identifier of the expense.
            event: The typed ExpenseEvent to fire.

        Returns:
            The result of the action as JSON.
        """
        return await self.fire_action(expense_id, event=event.value)

    async def get_model(self, expense_id: int) -> ExpenseModel:
        """Retrieves a single expense as a typed model.

        Args:
            expense_id: The identifier of the expense.

        Returns:
            An Expense model instance.
        """
        return _parse_model(await self.get(expense_id), ExpenseModel.from_dict)

    async def create(self, data: Mapping[str, Any]) -> JsonValue:
        """Creates a new expense.

        Args:
            data: The expense data.

        Returns:
            The created expense as JSON.
        """
        return await self._post_json("/accounts/{accountSlug}/expenses.json", data)

    async def update(self, expense_id: int, data: Mapping[str, Any]) -> JsonValue:
        """Updates an existing expense.

        Args:
            expense_id: The identifier of the expense.
            data: The update data.

        Returns:
            The updated expense as JSON.
        """
        return await self._patch_json(
            f"/accounts/{{accountSlug}}/expenses/{expense_id}.json",
            data,
        )

    async def delete(self, expense_id: int) -> JsonValue:
        """Deletes an expense.

        Args:
            expense_id: The identifier of the expense.

        Returns:
            The deleted expense data as JSON.
        """
        return await self._delete_json(f"/accounts/{{accountSlug}}/expenses/{expense_id}.json")

    async def create_payment(
        self,
        expense_id: int,
        data: Mapping[str, Any] | None = None,
    ) -> JsonValue:
        """Records a payment for an expense.

        Args:
            expense_id: The identifier of the expense.
            data: Optional payment data.

        Returns:
            The created payment as JSON.
        """
        return await self._post_json(
            f"/accounts/{{accountSlug}}/expenses/{expense_id}/payments.json",
            data or {},
        )

    async def delete_payment(self, expense_id: int, payment_id: int) -> JsonValue:
        """Deletes an expense payment.

        Args:
            expense_id: The identifier of the expense.
            payment_id: The identifier of the payment.

        Returns:
            The deleted payment data as JSON.
        """
        return await self._delete_json(
            f"/accounts/{{accountSlug}}/expenses/{expense_id}/payments/{payment_id}.json"
        )
