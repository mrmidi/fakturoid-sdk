from __future__ import annotations

import builtins
from collections.abc import AsyncIterator, Mapping, Sequence
from typing import Any, cast

from fakturoid_sdk.enums import InvoiceEvent, InvoiceStatus
from fakturoid_sdk.models import Invoice as InvoiceModel
from fakturoid_sdk.types import DateLike, JsonValue

from .base import _clean_params, _parse_model, _parse_models, _Resource


class Invoices(_Resource):
    """Fakturoid Invoices resource."""

    async def list(
        self,
        *,
        since: DateLike | None = None,
        until: DateLike | None = None,
        updated_since: DateLike | None = None,
        updated_until: DateLike | None = None,
        page: int | None = None,
        subject_id: int | None = None,
        custom_id: str | None = None,
        number: str | None = None,
        status: str | InvoiceStatus | None = None,
        document_type: str | None = None,
    ) -> JsonValue:
        """Lists invoices.

        Args:
            since: Filter by invoice date.
            until: Filter by invoice date.
            updated_since: Filter by last update date.
            updated_until: Filter by last update date.
            page: Page number for pagination.
            subject_id: Filter by subject identifier.
            custom_id: Filter by custom identifier.
            number: Filter by invoice number.
            status: Filter by invoice status.
            document_type: Filter by document type (e.g., 'invoice', 'proforma').

        Returns:
            The list of invoices as JSON.
        """
        params = _clean_params(
            since=since,
            until=until,
            updated_since=updated_since,
            updated_until=updated_until,
            page=page,
            subject_id=subject_id,
            custom_id=custom_id,
            number=number,
            status=status,
            document_type=document_type,
        )
        return await self._get_json("/accounts/{accountSlug}/invoices.json", params)

    async def search(
        self,
        *,
        query: str,
        page: int | None = None,
        tags: str | Sequence[str] | None = None,
    ) -> JsonValue:
        """Searches for invoices.

        Args:
            query: Search query string.
            page: Page number for pagination.
            tags: Filter by tags.

        Returns:
            The search results as JSON.
        """
        params = _clean_params(query=query, page=page, tags=tags)
        return await self._get_json("/accounts/{accountSlug}/invoices/search.json", params)

    async def get(self, invoice_id: int) -> JsonValue:
        """Retrieves a single invoice.

        Args:
            invoice_id: The identifier of the invoice.

        Returns:
            The invoice data as JSON.
        """
        return await self._get_json(f"/accounts/{{accountSlug}}/invoices/{invoice_id}.json")

    async def get_pdf(self, invoice_id: int) -> bytes:
        """Downloads the PDF of an invoice.

        Args:
            invoice_id: The identifier of the invoice.

        Returns:
            The PDF content as bytes.
        """
        return await self._get_bytes(
            f"/accounts/{{accountSlug}}/invoices/{invoice_id}/download.pdf"
        )

    async def get_attachment(self, invoice_id: int, attachment_id: int) -> bytes:
        """Downloads an invoice attachment.

        Args:
            invoice_id: The identifier of the invoice.
            attachment_id: The identifier of the attachment.

        Returns:
            The attachment content as bytes.
        """
        return await self._get_bytes(
            f"/accounts/{{accountSlug}}/invoices/{invoice_id}/attachments/{attachment_id}/download"
        )

    async def fire_action(self, invoice_id: int, *, event: str) -> JsonValue:
        """Fires a workflow event on an invoice.

        Args:
            invoice_id: The identifier of the invoice.
            event: The action event to fire.

        Returns:
            The result of the action as JSON.
        """
        return await self._post_json(
            f"/accounts/{{accountSlug}}/invoices/{invoice_id}/fire.json",
            {"event": event},
        )

    async def fire(self, invoice_id: int, *, event: InvoiceEvent) -> JsonValue:
        """Fires a typed workflow event on an invoice.

        Args:
            invoice_id: The identifier of the invoice.
            event: The typed InvoiceEvent to fire.

        Returns:
            The result of the action as JSON.
        """
        return await self.fire_action(invoice_id, event=event.value)

    async def get_model(self, invoice_id: int) -> InvoiceModel:
        """Retrieves a single invoice as a typed model.

        Args:
            invoice_id: The identifier of the invoice.

        Returns:
            An Invoice model instance.
        """
        return _parse_model(await self.get(invoice_id), InvoiceModel.from_dict)

    async def list_models(
        self,
        *,
        since: DateLike | None = None,
        until: DateLike | None = None,
        updated_since: DateLike | None = None,
        updated_until: DateLike | None = None,
        page: int | None = None,
        subject_id: int | None = None,
        custom_id: str | None = None,
        number: str | None = None,
        status: str | InvoiceStatus | None = None,
        document_type: str | None = None,
    ) -> builtins.list[InvoiceModel]:
        """Lists invoices as typed models.

        Args:
            since: Filter by invoice date.
            until: Filter by invoice date.
            updated_since: Filter by last update date.
            updated_until: Filter by last update date.
            page: Page number for pagination.
            subject_id: Filter by subject identifier.
            custom_id: Filter by custom identifier.
            number: Filter by invoice number.
            status: Filter by invoice status.
            document_type: Filter by document type.

        Returns:
            A list of Invoice model instances.
        """
        return _parse_models(
            await self.list(
                since=since,
                until=until,
                updated_since=updated_since,
                updated_until=updated_until,
                page=page,
                subject_id=subject_id,
                custom_id=custom_id,
                number=number,
                status=status,
                document_type=document_type,
            ),
            InvoiceModel.from_dict,
        )

    async def iter_list(
        self,
        *,
        since: DateLike | None = None,
        until: DateLike | None = None,
        updated_since: DateLike | None = None,
        updated_until: DateLike | None = None,
        start_page: int = 1,
        subject_id: int | None = None,
        custom_id: str | None = None,
        number: str | None = None,
        status: str | InvoiceStatus | None = None,
        document_type: str | None = None,
    ) -> AsyncIterator[JsonValue]:
        """Iterates over all invoices using pagination.

        Returns:
            An async iterator yielding invoice data as JSON.
        """
        params = _clean_params(
            since=since,
            until=until,
            updated_since=updated_since,
            updated_until=updated_until,
            subject_id=subject_id,
            custom_id=custom_id,
            number=number,
            status=status,
            document_type=document_type,
        )
        async for item in self._iter_list_items(
            "/accounts/{accountSlug}/invoices.json",
            params,
            start_page=start_page,
        ):
            yield item

    async def iter_models(
        self,
        *,
        since: DateLike | None = None,
        until: DateLike | None = None,
        updated_since: DateLike | None = None,
        updated_until: DateLike | None = None,
        start_page: int = 1,
        subject_id: int | None = None,
        custom_id: str | None = None,
        number: str | None = None,
        status: str | InvoiceStatus | None = None,
        document_type: str | None = None,
    ) -> AsyncIterator[InvoiceModel]:
        """Iterates over all invoices as typed models using pagination.

        Returns:
            An async iterator yielding Invoice model instances.
        """
        async for item in self.iter_list(
            since=since,
            until=until,
            updated_since=updated_since,
            updated_until=updated_until,
            start_page=start_page,
            subject_id=subject_id,
            custom_id=custom_id,
            number=number,
            status=status,
            document_type=document_type,
        ):
            if not isinstance(item, dict):
                raise TypeError(
                    f"Expected invoice list items to be objects, got {type(item).__name__}"
                )
            yield InvoiceModel.from_dict(cast(Mapping[str, Any], item))

    async def create(self, data: Mapping[str, Any]) -> JsonValue:
        """Creates a new invoice.

        Args:
            data: The invoice data.

        Returns:
            The created invoice as JSON.
        """
        return await self._post_json("/accounts/{accountSlug}/invoices.json", data)

    async def update(self, invoice_id: int, data: Mapping[str, Any]) -> JsonValue:
        """Updates an existing invoice.

        Args:
            invoice_id: The identifier of the invoice.
            data: The update data.

        Returns:
            The updated invoice as JSON.
        """
        return await self._patch_json(
            f"/accounts/{{accountSlug}}/invoices/{invoice_id}.json",
            data,
        )

    async def delete(self, invoice_id: int) -> JsonValue:
        """Deletes an invoice.

        Args:
            invoice_id: The identifier of the invoice.

        Returns:
            The deleted invoice data as JSON.
        """
        return await self._delete_json(f"/accounts/{{accountSlug}}/invoices/{invoice_id}.json")

    async def create_payment(
        self,
        invoice_id: int,
        data: Mapping[str, Any] | None = None,
    ) -> JsonValue:
        """Records a payment for an invoice.

        Args:
            invoice_id: The identifier of the invoice.
            data: Optional payment data.

        Returns:
            The created payment as JSON.
        """
        return await self._post_json(
            f"/accounts/{{accountSlug}}/invoices/{invoice_id}/payments.json",
            data or {},
        )

    async def create_tax_document(
        self,
        invoice_id: int,
        payment_id: int,
        data: Mapping[str, Any] | None = None,
    ) -> JsonValue:
        """Creates a tax document for an invoice payment.

        Args:
            invoice_id: The identifier of the invoice.
            payment_id: The identifier of the payment.
            data: Optional tax document data.

        Returns:
            The created tax document as JSON.
        """
        return await self._post_json(
            f"/accounts/{{accountSlug}}/invoices/{invoice_id}/payments/{payment_id}/create_tax_document.json",
            data or {},
        )

    async def delete_payment(self, invoice_id: int, payment_id: int) -> JsonValue:
        """Deletes an invoice payment.

        Args:
            invoice_id: The identifier of the invoice.
            payment_id: The identifier of the payment.

        Returns:
            The deleted payment data as JSON.
        """
        return await self._delete_json(
            f"/accounts/{{accountSlug}}/invoices/{invoice_id}/payments/{payment_id}.json"
        )

    async def create_message(
        self,
        invoice_id: int,
        data: Mapping[str, Any] | None = None,
    ) -> JsonValue:
        """Sends an email message associated with an invoice.

        Args:
            invoice_id: The identifier of the invoice.
            data: Message data (recipient, subject, body).

        Returns:
            The created message as JSON.
        """
        return await self._post_json(
            f"/accounts/{{accountSlug}}/invoices/{invoice_id}/message.json",
            data or {},
        )
