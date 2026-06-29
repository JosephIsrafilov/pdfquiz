import pytest

def test_login_rate_limit(client):
    """Test that rate limiting works on /login."""
    for i in range(6):
        resp = client.get("/login")
    assert resp.status_code == 429
