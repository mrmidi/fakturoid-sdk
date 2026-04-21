from __future__ import annotations

from fakturoid_sdk.types import DateLike, JsonValue

from .base import _clean_params, _Resource


class Events(_Resource):
    """Fakturoid Events resource."""

    async def list(
        self,
        *,
        subject_id: int | None = None,
        since: DateLike | None = None,
        page: int | None = None,
    ) -> JsonValue:
        """Lists all events.

        Args:
            subject_id: Optional subject identifier to filter by.
            since: Optional date to filter events from.
            page: Optional page number for pagination.

        Returns:
            The list of events as JSON.
        """
        params = _clean_params(subject_id=subject_id, since=since, page=page)
        return await self._get_json("/accounts/{accountSlug}/events.json", params)

    async def list_paid(
        self,
        *,
        subject_id: int | None = None,
        since: DateLike | None = None,
        page: int | None = None,
    ) -> JsonValue:
        """Lists only 'paid' events.

        Args:
            subject_id: Optional subject identifier to filter by.
            since: Optional date to filter events from.
            page: Optional page number for pagination.

        Returns:
            The list of paid events as JSON.
        """
        params = _clean_params(subject_id=subject_id, since=since, page=page)
        return await self._get_json("/accounts/{accountSlug}/events/paid.json", params)
