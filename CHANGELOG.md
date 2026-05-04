# Changelog

## [0.2.1] — 2026-05-04

### Added

- `Invoices.find_by_custom_id()` to easily retrieve a specific invoice by custom identifier.

### Fixed

- `Dispatcher` now correctly serializes explicit empty dictionaries (`{}`) into JSON payloads instead of dropping the request body.

## [0.2.0] — 2026-05-04

### Breaking

- `FakturoidClient` now requires a non-empty `user_agent` string. Passing an empty or whitespace-only string raises `ValueError`.
- `AuthProvider` now requires `user_agent` as a keyword-only argument. All direct instantiations must be updated.
- `Invoices.get_pdf()` raises `PdfNotReadyError` on 204 No Content instead of returning empty bytes.
- Removed `InvoiceEvent.PAY`. Use `Invoices.create_payment()` for recording payments.

### Added

- `Invoices.get_pdf_or_none()` — returns `None` when PDF is not ready (204), bytes when ready (200).
- `Invoices.wait_for_pdf()` — polls with configurable `attempts` and `delay_seconds` until PDF is ready.
- `Invoices.create_correction()` — helper to create correction documents with correct `document_type` and `correction_id`.
- `Expenses.list(document_type=...)` — filter expenses by document type.
- POST query parameter support in `_Resource._post_json()` via `Dispatcher.post(query_params=...)`.
- `PdfNotReadyError` is now exported from the package root (`from fakturoid_sdk import PdfNotReadyError`).
- `User-Agent` header is now sent on OAuth token and revoke requests (previously only sent on resource API requests).

### Fixed

- Invoice and expense `fire_action()` now sends `event` as a query parameter, matching the official Fakturoid API v3 spec (was incorrectly sent as a JSON body).
- `_Resource._post_json()` now uses explicit keyword argument `data=data` in the dispatcher call.
- README Basic Usage example now shows full client initialization and correct keyword-only `fire_action(event=...)` syntax.
- PDF polling example now includes `import asyncio`.

## [0.1.0] — 2026-04-01

- Initial release.
