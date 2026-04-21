from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from fakturoid_sdk.models import Subject as SubjectModel
from fakturoid_sdk.types import DateLike, JsonValue

from .base import _clean_params, _parse_model, _Resource


class Subjects(_Resource):
    """Fakturoid Subjects (Contacts) resource."""

    async def list(
        self,
        *,
        since: DateLike | None = None,
        updated_since: DateLike | None = None,
        page: int | None = None,
        custom_id: str | None = None,
    ) -> JsonValue:
        """Lists subjects.

        Args:
            since: Filter by date.
            updated_since: Filter by update date.
            page: Page number for pagination.
            custom_id: Filter by custom identifier.

        Returns:
            The list of subjects as JSON.
        """
        params = _clean_params(
            since=since,
            updated_since=updated_since,
            page=page,
            custom_id=custom_id,
        )
        return await self._get_json("/accounts/{accountSlug}/subjects.json", params)

    async def search(self, *, query: str, page: int | None = None) -> JsonValue:
        """Searches for subjects.

        Args:
            query: Search query string.
            page: Page number for pagination.

        Returns:
            The search results as JSON.
        """
        params = _clean_params(query=query, page=page)
        return await self._get_json("/accounts/{accountSlug}/subjects/search.json", params)

    async def get(self, subject_id: int) -> JsonValue:
        """Retrieves a single subject.

        Args:
            subject_id: The identifier of the subject.

        Returns:
            The subject data as JSON.
        """
        return await self._get_json(f"/accounts/{{accountSlug}}/subjects/{subject_id}.json")

    async def get_model(self, subject_id: int) -> SubjectModel:
        """Retrieves a single subject as a typed model.

        Args:
            subject_id: The identifier of the subject.

        Returns:
            A Subject model instance.
        """
        return _parse_model(await self.get(subject_id), SubjectModel.from_dict)

    async def create(self, data: Mapping[str, Any]) -> JsonValue:
        """Creates a new subject.

        Args:
            data: The subject data.

        Returns:
            The created subject as JSON.
        """
        return await self._post_json("/accounts/{accountSlug}/subjects.json", data)

    async def update(self, subject_id: int, data: Mapping[str, Any]) -> JsonValue:
        """Updates an existing subject.

        Args:
            subject_id: The identifier of the subject.
            data: The update data.

        Returns:
            The updated subject as JSON.
        """
        return await self._patch_json(
            f"/accounts/{{accountSlug}}/subjects/{subject_id}.json",
            data,
        )

    async def delete(self, subject_id: int) -> JsonValue:
        """Deletes a subject.

        Args:
            subject_id: The identifier of the subject.

        Returns:
            The deleted subject data as JSON.
        """
        return await self._delete_json(f"/accounts/{{accountSlug}}/subjects/{subject_id}.json")
