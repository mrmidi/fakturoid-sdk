# Fakturoid Python SDK

<p align=center>
  <a href="https://github.com/mrmidi/fakturoid-sdk/actions/workflows/ci.yml">
    <img src="https://github.com/mrmidi/fakturoid-sdk/actions/workflows/ci.yml/badge.svg" alt="CI Status">
  </a>
  <a href="https://github.com/mrmidi/fakturoid-sdk/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/mrmidi/fakturoid-sdk" alt="License">
  </a>
  <a href="https://github.com/astral-sh/uv">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json" alt="uv">
  </a>
  <a href="https://github.com/astral-sh/ruff">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff">
  </a>
  <a href="https://deepwiki.com/mrmidi/fakturoid-sdk">
    <img src="https://deepwiki.com/badge.svg" alt="Ask DeepWiki">
  </a>
</p>

A modern, typed, and **async-first** Python SDK for [Fakturoid.cz](https://www.fakturoid.cz/). 

This library is a Python rewrite of the [official Fakturoid PHP library](https://github.com/fakturoid/fakturoid-php), serving as a core logic reference. It provides an idiomatic Python experience with full `asyncio` support and strict typing.

Please see the [official API documentation](https://www.fakturoid.cz/api/v3) for detailed information about the endpoints.

> **Note:** We highly recommend creating a new account specifically for API testing and using a separate user (created via "Settings > User account") for production usage.

---

## Content

- [Installation](#installation)
- [Authorization](#authorization-by-oauth-20)
- [Usage](#usage)
  - [Basic Usage](#basic-usage)
  - [Switching Accounts](#switch-account)
  - [Downloading PDF](#downloading-an-invoice-pdf)
  - [Using custom_id](#using-custom_id)
  - [Inventory Resources](#inventory-resources)
  - [Recurring Generators](#recurring-generators)
- [Rate Limiting](#rate-limiting)
- [Handling Errors](#handling-errors)
- [Development](#development)

---

## Installation

Currently, the library is available directly from GitHub.

### Using pip
```bash
python -m pip install git+https://github.com/mrmidi/fakturoid-sdk.git
```

### Using uv
```bash
uv add git+https://github.com/mrmidi/fakturoid-sdk.git
```

---

## Authorization by OAuth 2.0

### Authorization Code Flow
Suitable for applications where users log in with their own Fakturoid credentials.

1. **Get Authentication URL**:
   ```python
   from fakturoid_sdk import FakturoidClient

   async with FakturoidClient(
       client_id='{fakturoid-client-id}',
       client_secret='{fakturoid-client-secret}',
       redirect_uri='{your-redirect-uri}'
   ) as fakturoid:
       auth_url = fakturoid.auth.get_authentication_url(state="optional-state")
       print(f"Please authorize here: {auth_url}")
   ```

2. **Process callback**:
   After the user is redirected back to your URI with a `code`:
   ```python
   await fakturoid.auth.request_credentials(code_from_url)
   ```

### Client Credentials Flow
Suitable for server-to-server communication where a user context is not required.
```python
from fakturoid_sdk import AuthType, FakturoidClient

async with FakturoidClient(
    client_id='{fakturoid-client-id}',
    client_secret='{fakturoid-client-secret}',
    account_slug='{fakturoid-account-slug}'
) as fakturoid:
    await fakturoid.auth.auth(AuthType.CLIENT_CREDENTIALS_CODE_FLOW)
```

### Credentials Callback
The SDK automatically refreshes expired tokens. Use a callback to persist updated credentials:

```python
def on_credentials_changed(credentials):
    if credentials:
        # Save to DB: credentials.access_token, credentials.refresh_token, etc.
        print(f"New access token obtained: {credentials.access_token}")

fakturoid.auth.set_credentials_callback(on_credentials_changed)
```

---

## Usage

### Basic Usage
```python
# Initialize and authenticate
await fManager.auth.auth(AuthType.CLIENT_CREDENTIALS_CODE_FLOW)

# Create a subject
subject = await fManager.subjects.create({'name': 'Firma s.r.o.', 'email': 'aloha@pokus.cz'})

# Create an invoice with lines
lines = [{'name': 'Big sale', 'quantity': 1, 'unit_price': 1000}]
invoice = await fManager.invoices.create({'subject_id': subject['id'], 'lines': lines})

# Send by email
await fManager.invoices.create_message(invoice['id'], {'email': 'aloha@pokus.cz'})

# Mark as paid
await fManager.invoices.create_payment(invoice['id'], {'paid_on': '2026-04-21'})

# Lock invoice
await fManager.invoices.fire_action(invoice['id'], 'lock')
```

### Switch account
You can change the account context without re-authenticating (provided the user has access to both).

```python
# Initial account
fManager.set_account_slug('company-a')
await fManager.bank_accounts.list()

# Switch to another account
fManager.set_account_slug('company-b')
await fManager.bank_accounts.list()
```

### Downloading an invoice PDF
Non-JSON endpoints return raw `bytes`. 

**Important:** If you request a PDF immediately after creating an invoice, you might receive a `204 No Content` (empty body) because the PDF isn't generated yet.

```python
import asyncio

async def download_invoice(invoice_id):
    while True:
        # In a real app, use a more defensive loop or a background task
        response = await fManager.dispatcher.get(f"/accounts/{{accountSlug}}/invoices/{invoice_id}/download.pdf")
        
        if response.get_status_code() == 200:
            with open(f"invoice_{invoice_id}.pdf", "wb") as f:
                f.write(response.get_bytes())
            break
        
        await asyncio.sleep(1)
```

### Using `custom_id`
Store your application's internal record ID in Fakturoid using the `custom_id` attribute.

```python
# Filter by custom_id
response = await fManager.subjects.list(custom_id='10')
if response:
    subject = response[0]
```

### Inventory Resources

**Inventory Items**:
```python
# List items with filters
await fManager.inventory_items.list(sku='SKU1234', article_number='IAN321')

# Search items
await fManager.inventory_items.search(query='Item name')

# CRUD
await fManager.inventory_items.create({
    'name': 'Item name',
    'sku': 'SKU12345',
    'track_quantity': True,
    'quantity': 100
})
await fManager.inventory_items.archive(item_id)
```

**Inventory Moves**:
```python
# Create stock-in move
await fManager.inventory_moves.create(item_id, {
    'direction': 'in',
    'quantity_change': 5,
    'purchase_price': '249.99'
})
```

### Recurring Generators
```python
# Pause a generator
await fManager.recurring_generators.pause(generator_id)

# Activate with a specific next occurrence
await fManager.recurring_generators.activate(generator_id, {
    'next_occurrence_on': '2026-05-01'
})
```

---

## Rate Limiting

The SDK provides methods to inspect your rate limit status directly from the response or via exceptions:

```python
from fakturoid_sdk import ClientError

try:
    # Use the dispatcher directly to get the Response object
    resp = await fManager.dispatcher.get("/accounts/{accountSlug}/account.json")
    print(f"Quota: {resp.get_rate_limit_quota()}")
    print(f"Remaining: {resp.get_rate_limit_remaining()}")
    
except ClientError as e:
    if e.is_rate_limit_exceeded():
        # Reset time in seconds
        reset_time = e.response.get_rate_limit_reset()
        print(f"Rate limit exceeded. Try again in {reset_time}s.")
```

---

## Handling Errors

The library raises `ClientError` for 4xx statuses and `ServerError` for 5xx.

```python
from fakturoid_sdk import ClientError, ServerError

try:
    await fManager.subjects.create({'name': ''})
except ClientError as e:
    print(f"Status: {e.status_code}") # 422
    # The API returns error details in the body
    error_data = e.response.get_body(return_json_as_dict=True)
    print(error_data['errors']) 
except ServerError as e:
    print("Fakturoid is temporarily unavailable.")
```

---

## Development

### Setup with uv
```bash
git clone https://github.com/mrmidi/fakturoid-sdk.git
cd fakturoid-sdk
uv sync
```

### Testing & Linting
```bash
uv run pytest       # Run tests
uv run ruff check . # Lint
uv run mypy src     # Type check
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
