import pytest

def test_security_headers(client):
    """Test that security headers are present on responses."""
    resp = client.get("/")
    headers = resp.headers
    assert headers.get("X-Content-Type-Options") == "nosniff"
    assert headers.get("X-Frame-Options") == "DENY"
    assert headers.get("Referrer-Policy") == "same-origin"
    assert "default-src 'self'" in headers.get("Content-Security-Policy", "")
    # In tests, debug is usually false, but testing=True. The header HSTS relies on not app.debug.
    # We can check if HSTS is set if app.debug is false.
    # Actually in conftest.py we don't set app.debug=True, so HSTS should be there
    assert "Strict-Transport-Security" in headers
