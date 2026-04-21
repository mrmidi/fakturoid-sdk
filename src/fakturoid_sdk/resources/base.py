from __future__ import annotations

import datetime as dt
from collections.abc import AsyncIterator, Callable, Mapping
from enum import Enum
from typing import Any, TypeVar, cast

from fakturoid_sdk.dispatcher import Dispatcher
from fakturoid_sdk.response import Response
from fakturoid_sdk.types import JsonValue

TModel = TypeVar("TModel")


def _coerce_param_value(value: Any) -> Any:
    """Coerces a parameter value to a format suitable for the API."""
    if isinstance(value, Enum):
        return value.value

    # `datetime` is also a `date`; check `datetime` first.
    if isinstance(value, dt.datetime):
        return value.isoformat()
    if isinstance(value, dt.date):
        return value.isoformat()

    if isinstance(value, list | tuple):
        return [_coerce_param_value(v) for v in value]

    return value


def _clean_params(**kwargs: Any) -> dict[str, Any]:
    """Filters out None values and coerces parameter values."""
    return {k: _coerce_param_value(v) for k, v in kwargs.items() if v is not None}


def _json(response: Response) -> JsonValue:
    """Extracts JSON body from a Response."""
    return cast(JsonValue, response.get_body(return_json_as_dict=True))


def _parse_model(data: JsonValue, factory: Callable[[Mapping[str, Any]], TModel]) -> TModel:
    """Parses a JSON object into a model instance."""
    if not isinstance(data, dict):
        raise TypeError(f"Expected object response, got {type(data).__name__}")
    return factory(cast(Mapping[str, Any], data))


def _parse_models(data: JsonValue, factory: Callable[[Mapping[str, Any]], TModel]) -> list[TModel]:
    """Parses a JSON list of objects into a list of model instances."""
    if not isinstance(data, list):
        raise TypeError(f"Expected list response, got {type(data).__name__}")
    models: list[TModel] = []
    for item in data:
        if not isinstance(item, dict):
            raise TypeError(f"Expected list items to be objects, got {type(item).__name__}")
        models.append(factory(cast(Mapping[str, Any], item)))
    return models


class _Resource:
    """Base class for all Fakturoid resources."""

    def __init__(self, dispatcher: Dispatcher) -> None:
        """Initializes the resource.

        Args:
            dispatcher: The dispatcher to use for API requests.
        """
        self._dispatcher = dispatcher

    async def _get_json(self, path: str, params: Mapping[str, Any] | None = None) -> JsonValue:
        """Performs a GET request and returns JSON."""
        return _json(await self._dispatcher.get(path, params))

    async def _post_json(self, path: str, data: Mapping[str, Any] | None = None) -> JsonValue:
        """Performs a POST request and returns JSON."""
        return _json(await self._dispatcher.post(path, data))

    async def _patch_json(self, path: str, data: Mapping[str, Any]) -> JsonValue:
        """Performs a PATCH request and returns JSON."""
        return _json(await self._dispatcher.patch(path, data))

    async def _delete_json(self, path: str) -> JsonValue:
        """Performs a DELETE request and returns JSON."""
        return _json(await self._dispatcher.delete(path))

    async def _get_bytes(self, path: str, params: Mapping[str, Any] | None = None) -> bytes:
        """Performs a GET request and returns raw bytes."""
        return (await self._dispatcher.get(path, params)).get_bytes()

    async def _iter_list_items(
        self,
        path: str,
        params: Mapping[str, Any] | None = None,
        *,
        start_page: int = 1,
        page_param: str = "page",
    ) -> AsyncIterator[JsonValue]:
        """Iterates over all items in a paginated resource."""
        page = start_page
        base_params = dict(params or {})

        while True:
            page_params = dict(base_params)
            page_params[page_param] = page

            data = await self._get_json(path, page_params)
            if not isinstance(data, list):
                raise TypeError(
                    f"Expected paginated list response from {path!r}, got {type(data).__name__}"
                )
            if not data:
                return

            for item in data:
                yield cast(JsonValue, item)
            page += 1
