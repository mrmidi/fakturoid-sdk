from decimal import Decimal

from fakturoid_sdk.models import Invoice


def test_invoice_model_common_fields() -> None:
    invoice = Invoice.from_dict(
        {
            "correction_id": 10,
            "related_id": 11,
            "issued_on": "2026-05-04",
            "due_on": "2026-05-18",
            "document_type": "invoice",
            "currency": "CZK",
            "subtotal": "1000.50",
            "total": "1210.60",
            "remaining_amount": "1210.60",
            "remaining_native_amount": "1210.60",
            "native_subtotal": "1000.50",
            "native_total": "1210.60",
            "lines": [{"name": "Repair"}],
            "payments": [{"id": 1}],
            "attachments": [{"id": 2}],
            "html_url": "https://example.com/html",
            "public_html_url": "https://example.com/public",
            "url": "https://example.com/api",
            "pdf_url": "https://example.com/pdf",
        }
    )

    assert invoice.correction_id == 10
    assert invoice.related_id == 11
    assert invoice.issued_on is not None
    assert invoice.issued_on.isoformat() == "2026-05-04"
    assert invoice.due_on is not None
    assert invoice.due_on.isoformat() == "2026-05-18"
    assert invoice.document_type == "invoice"
    assert invoice.currency == "CZK"
    assert invoice.subtotal == Decimal("1000.50")
    assert invoice.total == Decimal("1210.60")
    assert invoice.remaining_amount == Decimal("1210.60")
    assert invoice.remaining_native_amount == Decimal("1210.60")
    assert invoice.native_subtotal == Decimal("1000.50")
    assert invoice.native_total == Decimal("1210.60")
    assert invoice.lines == [{"name": "Repair"}]
    assert invoice.payments == [{"id": 1}]
    assert invoice.attachments == [{"id": 2}]
    assert invoice.html_url == "https://example.com/html"
    assert invoice.public_html_url == "https://example.com/public"
    assert invoice.url == "https://example.com/api"
    assert invoice.pdf_url == "https://example.com/pdf"


def test_invoice_model_common_fields_tolerate_invalid_values() -> None:
    invoice = Invoice.from_dict(
        {
            "issued_on": "bad-date",
            "total": "bad-decimal",
            "lines": {"bad": "shape"},
        }
    )

    assert invoice.issued_on is None
    assert invoice.total is None
    assert invoice.lines == []
