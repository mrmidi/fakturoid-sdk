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
</p>

A modern, typed, and **async-first** Python SDK for [Fakturoid.cz](https://www.fakturoid.cz/). 

This library is a Python rewrite of the [official Fakturoid PHP library](https://github.com/fakturoid/fakturoid-php), which served as the primary reference for core logic and unit test samples. It aims to provide a native, idiomatic Python experience while maintaining the robustness of the original implementation.

Please see the [official API documentation](https://www.fakturoid.cz/api/v3) for detailed information about the endpoints.

> **Note:** We highly recommend creating a new account specifically for API testing and using a separate user (created via "Settings > User account") for production usage.

---

## Features

- **Async-First**: Built from the ground up to support modern `asyncio` workflows.
- **Fully Typed**: Strict type hints and `mypy` compatibility for a better developer experience.
- **Modular Design**: Separated resource modules (Invoices, Expenses, Subjects, etc.) for easy navigation.
- **Production Grade**: Includes structured logging, automatic retries with exponential backoff, and comprehensive test coverage.
- **Modern Tooling**: Powered by `uv`, `ruff`, and `tenacity`.

## Installation

Currently, the library is available directly from GitHub. You can install it using `pip` or `uv`:

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

Authorization using OAuth takes place in several steps. We use data obtained from the developer portal as client ID and client secret (*Settings → Connect other apps → OAuth 2 for app developers*).

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
The SDK can automatically refresh expired tokens. Use a callback to persist updated credentials to your database:

```python
def save_credentials(credentials):
    if credentials:
        # Save to DB: credentials.access_token, credentials.refresh_token, etc.
        pass

fakturoid.auth.set_credentials_callback(save_credentials)
```

---

## Usage

### Basic Example
```python
import asyncio
from fakturoid_sdk import AuthType, FakturoidClient

async def main():
    async with FakturoidClient(
        client_id='{id}',
        client_secret='{secret}',
        account_slug='{slug}'
    ) as fManager:
        await fManager.auth.auth(AuthType.CLIENT_CREDENTIALS_CODE_FLOW)

        # Create a subject
        subject = await fManager.subjects.create({
            'name': 'Firma s.r.o.', 
            'email': 'aloha@pokus.cz'
        })
        
        # Create an invoice
        lines = [{'name': 'Big sale', 'quantity': 1, 'unit_price': 1000}]
        invoice_data = await fManager.invoices.create({
            'subject_id': subject['id'], 
            'lines': lines
        })
        
        # Mark as paid
        await fManager.invoices.create_payment(invoice_data['id'], {
            'paid_on': '2026-04-21'
        })

asyncio.run(main())
```

### Downloading a PDF
Due to the async nature, non-JSON endpoints return raw `bytes`.
```python
pdf_content = await fManager.invoices.get_pdf(invoice_id)
with open(f"invoice_{invoice_id}.pdf", "wb") as f:
    f.write(pdf_content)
```

### Typed Models (Optional)
If you prefer attribute access over dictionary keys:
```python
invoice = await fManager.invoices.get_model(invoice_id)
print(invoice.number, invoice.status, invoice.due_on)
```

### Pagination
Efficiently iterate over large datasets across multiple pages:
```python
from fakturoid_sdk import InvoiceStatus

async for invoice in fManager.invoices.iter_models(status=InvoiceStatus.OPEN):
    print(f"Processing {invoice.number}")
```

---

## Rate Limiting

The SDK provides access to rate limit headers through the response object (if using raw methods) or via custom exceptions:

```python
from fakturoid_sdk import ClientError

try:
    await fManager.invoices.list()
except ClientError as e:
    if e.is_rate_limit_exceeded():
        reset_time = e.response.get_rate_limit_reset()
        print(f"Rate limit hit. Retry in {reset_time} seconds.")
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
# Run tests
uv run pytest

# Run linting
uv run ruff check .

# Run type checking
uv run mypy src
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
