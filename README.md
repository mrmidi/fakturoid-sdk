
# fakturoid-sdk

Modern, typed, async-first Python SDK for the Fakturoid API.

## Install

Using `uv`:

```bash
uv add fakturoid-sdk
```

Using `pip`:

```bash
python -m pip install fakturoid-sdk
```

## Quickstart (async)

The recommended entrypoint is `FakturoidClient`, which wires auth + dispatcher and exposes
Pythonic resources (keyword args; returns `dict`/`list`/`bytes`/`None`).

```python
import asyncio

from fakturoid_sdk import AuthType, FakturoidClient


async def main() -> None:
	async with FakturoidClient(
		client_id="YOUR_CLIENT_ID",
		client_secret="YOUR_CLIENT_SECRET",
		account_slug="your-account-slug",
	) as fakturoid:
		# Client Credentials flow
		await fakturoid.auth.auth(AuthType.CLIENT_CREDENTIALS_CODE_FLOW)

		invoices = await fakturoid.invoices.list(page=1)
		print(invoices)


asyncio.run(main())
```

## Authorization Code flow

```python
from fakturoid_sdk import AuthType, FakturoidClient


async with FakturoidClient(
	client_id="YOUR_CLIENT_ID",
	client_secret="YOUR_CLIENT_SECRET",
	redirect_uri="https://example.com/oauth/callback",
	account_slug="your-account-slug",
) as fakturoid:
	url = fakturoid.auth.get_authentication_url(state="optional")
	print("Open:", url)

	# After redirect:
	fakturoid.auth.load_code("CODE_FROM_CALLBACK")
	await fakturoid.auth.auth(AuthType.AUTHORIZATION_CODE_FLOW)

	me = await fakturoid.account.get()
	print(me)
```

## Retries (optional)

Retries are **off by default**. If you enable them, the default config retries only `GET` calls and
only for transient failures (connection errors, 5xx, and optionally 429).

```python
from fakturoid_sdk import FakturoidClient, RetryConfig


retry = RetryConfig(max_attempts=3)

async with FakturoidClient(
	client_id="...",
	client_secret="...",
	account_slug="...",
	retry=retry,
) as fakturoid:
	...
```

## Downloads / non-JSON responses

For non-JSON endpoints (e.g., file downloads), the SDK returns `bytes`:

```python
data = await fakturoid.inbox_files.download(123)
```

## Pythonic params (dates + enums)

Most query params accept Python-native types:

```python
import datetime as dt

from fakturoid_sdk import InvoiceStatus

invoices = await fakturoid.invoices.list(
	since=dt.date(2026, 1, 1),
	status=InvoiceStatus.OPEN,
)
```

For fire-actions you can also use enums:

```python
from fakturoid_sdk import InvoiceEvent

await fakturoid.invoices.fire(123, event=InvoiceEvent.PAY)
```

## Typed models (optional convenience)

If you want typed accessors (while keeping the full response available), use `*_model` methods:

```python
invoice = await fakturoid.invoices.get_model(123)
print(invoice.id, invoice.status, invoice.due_on)
print(invoice.raw["html_url"])  # fields not modeled yet stay available
```

## Pagination helpers

List endpoints support async iteration across pages (stops when an empty page is returned):

```python
async for invoice in fakturoid.invoices.iter_models(status=InvoiceStatus.OPEN):
	print(invoice.id, invoice.number)
```

## Providers

`FakturoidClient` exposes resources as attributes:

- `account`, `bank_accounts`, `events`, `expenses`, `generators`, `inbox_files`
- `inventory_items`, `inventory_moves`, `invoices`, `number_formats`, `recurring_generators`
- `subjects`, `todos`, `users`, `webhooks`

