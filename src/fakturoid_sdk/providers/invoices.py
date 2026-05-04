from __future__ import annotations

from typing import Any

from fakturoid_sdk.dispatcher import Dispatcher
from fakturoid_sdk.response import Response

from .base import Provider


class InvoicesProvider(Provider):
    """Raw API provider for Invoices resource."""

    def __init__(self, dispatcher: Dispatcher) -> None:
        """Initializes the provider.

        Args:
            dispatcher: The dispatcher to use for API requests.
        """
        self._dispatcher = dispatcher

    async def list(self, params: dict[str, Any] | None = None) -> Response:
        """Lists invoices.

        Args:
            params: Optional query parameters (since, until, updated_since,
                updated_until, page, subject_id, custom_id, number, status,
                document_type).

        Returns:
            The raw API response.
        """
        allowed = [
            "since",
            "until",
            "updated_since",
            "updated_until",
            "page",
            "subject_id",
            "custom_id",
            "number",
            "status",
            "document_type",
        ]
        return await self._dispatcher.get(
            "/accounts/{accountSlug}/invoices.json",
            self.filter_options(params, allowed),
        )

    async def search(self, params: dict[str, Any] | None = None) -> Response:
        """Searches for invoices.

        Args:
            params: Optional query parameters (query, page, tags).

        Returns:
            The raw API response.
        """
        return await self._dispatcher.get(
            "/accounts/{accountSlug}/invoices/search.json",
            self.filter_options(params, ["query", "page", "tags"]),
        )

    async def get(self, invoice_id: int) -> Response:
        """Retrieves a single invoice.

        Args:
            invoice_id: The identifier of the invoice.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.get(f"/accounts/{{accountSlug}}/invoices/{invoice_id}.json")

    async def get_pdf(self, invoice_id: int) -> Response:
        """Downloads the PDF of an invoice.

        Args:
            invoice_id: The identifier of the invoice.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.get(
            f"/accounts/{{accountSlug}}/invoices/{invoice_id}/download.pdf"
        )

    async def get_attachment(self, invoice_id: int, attachment_id: int) -> Response:
        """Downloads an invoice attachment.

        Args:
            invoice_id: The identifier of the invoice.
            attachment_id: The identifier of the attachment.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.get(
            f"/accounts/{{accountSlug}}/invoices/{invoice_id}/attachments/{attachment_id}/download"
        )

    async def fire_action(self, invoice_id: int, event: str) -> Response:
        """Fires a workflow event on an invoice.

        Args:
            invoice_id: The identifier of the invoice.
            event: The action event to fire.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.post(
            f"/accounts/{{accountSlug}}/invoices/{invoice_id}/fire.json",
            query_params={"event": event},
        )

    async def create(self, data: dict[str, Any]) -> Response:
        """Creates a new invoice.

        Args:
            data: The invoice data.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.post("/accounts/{accountSlug}/invoices.json", data)

    async def update(self, invoice_id: int, data: dict[str, Any]) -> Response:
        """Updates an existing invoice.

        Args:
            invoice_id: The identifier of the invoice.
            data: The update data.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.patch(
            f"/accounts/{{accountSlug}}/invoices/{invoice_id}.json",
            data,
        )

    async def delete(self, invoice_id: int) -> Response:
        """Deletes an invoice.

        Args:
            invoice_id: The identifier of the invoice.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.delete(
            f"/accounts/{{accountSlug}}/invoices/{invoice_id}.json"
        )

    async def create_payment(self, invoice_id: int, data: dict[str, Any] | None = None) -> Response:
        """Records a payment for an invoice.

        Args:
            invoice_id: The identifier of the invoice.
            data: Optional payment data.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.post(
            f"/accounts/{{accountSlug}}/invoices/{invoice_id}/payments.json",
            data or {},
        )

    async def create_tax_document(
        self,
        invoice_id: int,
        payment_id: int,
        data: dict[str, Any] | None = None,
    ) -> Response:
        """Creates a tax document for an invoice payment.

        Args:
            invoice_id: The identifier of the invoice.
            payment_id: The identifier of the payment.
            data: Optional tax document data.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.post(
            f"/accounts/{{accountSlug}}/invoices/{invoice_id}/payments/{payment_id}/create_tax_document.json",
            data or {},
        )

    async def delete_payment(self, invoice_id: int, payment_id: int) -> Response:
        """Deletes an invoice payment.

        Args:
            invoice_id: The identifier of the invoice.
            payment_id: The identifier of the payment.

        Returns:
            The raw API response.
        """
        return await self._dispatcher.delete(
            f"/accounts/{{accountSlug}}/invoices/{invoice_id}/payments/{payment_id}.json"
        )

    async def create_message(self, invoice_id: int, data: dict[str, Any] | None = None) -> Response:
        """Sends an email message associated with an invoice.

        Args:
            invoice_id: The identifier of the invoice.
            data: Message data (recipient, subject, body).

        Returns:
            The raw API response.
        """
        return await self._dispatcher.post(
            f"/accounts/{{accountSlug}}/invoices/{invoice_id}/message.json",
            data or {},
        )
