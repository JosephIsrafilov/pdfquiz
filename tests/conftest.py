"""
Shared pytest fixtures for the PDF/DOCX Quiz test suite.
"""

import os
import tempfile
import pytest

# Tell the app to use an in-memory SQLite DB so tests don't touch app.db
os.environ.setdefault("DATABASE_URL", "")
_test_db = tempfile.NamedTemporaryFile(prefix="knowledge-check-tests-", suffix=".db", delete=False)
_test_db.close()
os.environ.setdefault("DB_PATH", _test_db.name)
os.environ.setdefault("SECRET_KEY", "test-secret-key")


@pytest.fixture(scope="session")
def app():
    """Create a Flask test application."""
    from app import create_app

    flask_app = create_app()
    flask_app.config["TESTING"] = True
    return flask_app


@pytest.fixture(scope="session")
def client(app):
    """Test client with CSRF bypass: inject the token into every POST."""
    _client = app.test_client()

    # Open a session so we can plant the CSRF token
    with _client.session_transaction() as sess:
        sess["csrf_token"] = "test-csrf-token"

    class CSRFClient:
        """Thin wrapper that auto-injects the CSRF token into POST/PUT/DELETE requests."""

        def __getattr__(self, name):
            orig = getattr(_client, name)
            if name in ("post", "put", "patch", "delete"):
                def method_with_csrf(*args, **kwargs):
                    # Add X-CSRFToken header
                    headers = dict(kwargs.pop("headers", {}) or {})
                    headers.setdefault("X-CSRFToken", "test-csrf-token")
                    # Also ensure the session has the token on every call
                    with _client.session_transaction() as sess:
                        sess["csrf_token"] = "test-csrf-token"
                    return orig(*args, headers=headers, **kwargs)
                return method_with_csrf
            return orig

        # Expose session_transaction directly
        def session_transaction(self):
            return _client.session_transaction()

        def get(self, *args, **kwargs):
            return _client.get(*args, **kwargs)

    return CSRFClient()

@pytest.fixture(autouse=True)
def reset_limiter():
    """Reset rate limiter before each test to prevent side effects."""
    try:
        from app.limiter import limiter
        limiter.reset()
    except Exception:
        pass

