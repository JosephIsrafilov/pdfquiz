import pytest
from flask import session

def test_session_cookie_security(app, client):
    """Test that session cookies are hardened."""
    # Ensure they are in app.config
    assert app.config["SESSION_COOKIE_HTTPONLY"] is True
    assert app.config["SESSION_COOKIE_SAMESITE"] == "Lax"
    # By default in testing, DEBUG is usually False (unless set), but let's check it's defined
    assert "SESSION_COOKIE_SECURE" in app.config

    # Let's hit a route that sets a session variable and check the Set-Cookie header
    @app.route("/set_session")
    def set_session():
        session["foo"] = "bar"
        return "OK"

    resp = client.get("/set_session")
    cookies = resp.headers.getlist("Set-Cookie")
    if cookies:
        cookie_str = cookies[0].lower()
        assert "httponly" in cookie_str
        assert "samesite=lax" in cookie_str
