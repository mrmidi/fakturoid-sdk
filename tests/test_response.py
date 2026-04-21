import httpx

from fakturoid_sdk.response import Response


def test_json_body_is_parsed_to_object() -> None:
    r = httpx.Response(
        200,
        headers={"Content-Type": "application/json; charset=utf-8"},
        content=b'{"name":"Test"}',
    )
    response = Response(r)

    assert response.get_status_code() == 200
    body = response.get_body()
    assert body.name == "Test"


def test_json_with_mixed_headers_case() -> None:
    r = httpx.Response(
        200,
        headers={"content-type": "application/json; charset=utf-8"},
        content=b'{"name":"Test"}',
    )
    response = Response(r)

    assert response.get_header("Content-Type") == "application/json; charset=utf-8"
    assert response.get_header("content-type") == "application/json; charset=utf-8"
    assert response.get_header("cOnTeNt-TyPe") == "application/json; charset=utf-8"

    body = response.get_body()
    assert body.name == "Test"


def test_other_body() -> None:
    r = httpx.Response(200, content=b"Test")
    response = Response(r)

    assert response.get_status_code() == 200
    assert response.get_header("Content-Type") is None
    assert response.get_bytes() == b"Test"
    assert response.get_body() == "Test"


def test_rate_limit_headers() -> None:
    r = httpx.Response(
        200,
        headers={
            "X-RateLimit-Policy": "default;q=400;w=60",
            "X-RateLimit": "default;r=398;t=55",
        },
        content=b"",
    )
    response = Response(r)

    assert response.get_rate_limit_quota() == 400
    assert response.get_rate_limit_window() == 60
    assert response.get_rate_limit_remaining() == 398
    assert response.get_rate_limit_reset() == 55


def test_rate_limit_headers_not_present() -> None:
    r = httpx.Response(200, content=b"")
    response = Response(r)

    assert response.get_rate_limit_quota() is None
    assert response.get_rate_limit_window() is None
    assert response.get_rate_limit_remaining() is None
    assert response.get_rate_limit_reset() is None
