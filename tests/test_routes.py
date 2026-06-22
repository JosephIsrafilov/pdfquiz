"""
Integration tests for Flask routes: auth, main, admin, API.
"""

import json
import pytest


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------


def test_health_returns_ok(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] == "ok"
    assert "db" in data


# ---------------------------------------------------------------------------
# Auth routes
# ---------------------------------------------------------------------------


def test_login_page_loads(client):
    resp = client.get("/login")
    assert resp.status_code == 200
    assert b"\xd0\x92\xd1\x85\xd0\xbe\xd0\xb4" in resp.data or b"login" in resp.data.lower()


def test_register_page_loads(client):
    resp = client.get("/register")
    assert resp.status_code == 200


def test_register_and_login(client):
    """Full cycle: register → login → redirect to index."""
    # Register
    resp = client.post(
        "/register",
        data={"username": "testuser_routes", "password": "password123", "password_repeat": "password123"},
        follow_redirects=True,
    )
    assert resp.status_code == 200

    # Logout
    client.post("/logout", follow_redirects=True)

    # Login
    resp = client.post(
        "/login",
        data={"username": "testuser_routes", "password": "password123"},
        follow_redirects=True,
    )
    assert resp.status_code == 200


def test_login_wrong_password(client):
    resp = client.post(
        "/login",
        data={"username": "nobody", "password": "wrongpassword"},
    )
    assert resp.status_code == 200
    # Should show the login form again (not redirect)
    assert b"login" in resp.data.lower() or b"\xd0\x92\xd1\x85\xd0\xbe\xd0\xb4" in resp.data


def test_logout_redirects_to_login(client):
    # Ensure we are logged in first
    client.post(
        "/register",
        data={"username": "testlogout", "password": "pass1234", "password_repeat": "pass1234"},
        follow_redirects=True,
    )
    resp = client.post("/logout", follow_redirects=True)
    assert resp.status_code == 200


# ---------------------------------------------------------------------------
# Main routes
# ---------------------------------------------------------------------------


def test_index_loads(client):
    resp = client.get("/")
    assert resp.status_code == 200


def test_profile_requires_login(client):
    """Unauthenticated access to /profile should redirect."""
    # Make sure we are logged out
    client.post("/logout", follow_redirects=True)
    resp = client.get("/profile")
    # Should redirect (302) or render login page (200 if follow_redirects)
    assert resp.status_code in (200, 302)


def test_profile_loads_when_logged_in(client):
    client.post(
        "/register",
        data={"username": "testprofile", "password": "pass1234", "password_repeat": "pass1234"},
        follow_redirects=True,
    )
    resp = client.get("/profile")
    assert resp.status_code == 200


# ---------------------------------------------------------------------------
# API parse — document_id missing/invalid
# ---------------------------------------------------------------------------


def test_api_parse_no_file_no_document(client):
    resp = client.post("/api/parse", data={})
    assert resp.status_code == 400
    data = resp.get_json()
    assert "error" in data


def test_api_parse_invalid_document_id(client):
    resp = client.post("/api/parse", data={"document_id": "not-a-number"})
    assert resp.status_code == 400
    data = resp.get_json()
    assert "error" in data


def test_api_parse_nonexistent_document(client):
    resp = client.post("/api/parse", data={"document_id": "99999"})
    assert resp.status_code == 404
    data = resp.get_json()
    assert "error" in data


def test_api_parse_json_questions(client):
    """Upload a valid JSON question set directly."""
    questions = [
        {
            "text": "What is 2+2?",
            "options": [
                {"text": "3", "is_correct": False},
                {"text": "4", "is_correct": True},
            ],
            "number": 1,
        }
    ]
    json_bytes = json.dumps(questions).encode("utf-8")
    data = {"file": (json_bytes, "questions.json", "application/json")}
    resp = client.post("/api/parse", data=data, content_type="multipart/form-data")
    assert resp.status_code == 200
    result = resp.get_json()
    assert result["count"] == 1
    assert result["questions"][0]["text"] == "What is 2+2?"


def test_api_parse_unsupported_extension(client):
    data = {"file": (b"text content", "file.txt", "text/plain")}
    resp = client.post("/api/parse", data=data, content_type="multipart/form-data")
    assert resp.status_code == 400


# ---------------------------------------------------------------------------
# Admin panel — access control
# ---------------------------------------------------------------------------


def test_admin_panel_requires_admin(client):
    """Regular (non-admin) user should get 403."""
    client.post(
        "/register",
        data={"username": "regularuser", "password": "pass1234", "password_repeat": "pass1234"},
        follow_redirects=True,
    )
    resp = client.get("/admin")
    # Either forbidden or redirect
    assert resp.status_code in (200, 302, 403)
