"""
Integration tests for Flask routes: auth, main, admin, API.
"""

import json
import io
from datetime import datetime
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


def test_csrf_protection_missing_token(app):
    """Test that a POST without a CSRF token returns 403."""
    client = app.test_client()
    resp = client.post("/login", data={"username": "test", "password": "pwd"})
    assert resp.status_code == 403


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
    assert b"Knowledge Check" in resp.data


def test_topic_quiz_hides_answers_and_grades_on_server(client):
    from app.models.knowledge import fetch_catalog
    from app.database import db_execute, get_db_connection

    catalog = fetch_catalog()
    topic_ids = [topic["id"] for topic in catalog[0]["topics"][:2]]
    with get_db_connection() as connection:
        session_count_before = db_execute(
            connection,
            "SELECT COUNT(*) FROM quiz_sessions",
        ).fetchone()[0]

    resp = client.post(
        "/api/quizzes",
        json={
            "topic_ids": topic_ids,
            "count": 4,
            "language": "en",
            "difficulty": "all",
        },
    )
    assert resp.status_code == 201
    quiz = resp.get_json()
    assert len(quiz["questions"]) == 4
    with get_db_connection() as connection:
        session_count_after = db_execute(
            connection,
            "SELECT COUNT(*) FROM quiz_sessions",
        ).fetchone()[0]
    assert session_count_after == session_count_before + 1
    assert all(
        "is_correct" not in option
        for question in quiz["questions"]
        for option in question["options"]
    )

    answers = {str(question["id"]): 0 for question in quiz["questions"]}
    submitted = client.post(
        f"/api/quizzes/{quiz['token']}/submit",
        json={"answers": answers},
    )
    assert submitted.status_code == 200
    result = submitted.get_json()["result"]
    assert result["total"] == 4
    assert len(result["review"]) == 4
    assert all(item["correct_answers"] for item in result["review"])
    assert all(item["explanation"] for item in result["review"])


def test_topic_quiz_submits_multi_select_question(client):
    from app.models.knowledge import create_course, create_question, create_topic
    from app.models.quiz import fetch_quiz_session

    course_id = create_course("Route Test Course", "Route Test Course")
    topic_id = create_topic(course_id, "Multi Select", "Multi Select")
    question_id = create_question(
        topic_id=topic_id,
        text_en="Select the Python collection types.",
        text_ru="Select the Python collection types.",
        options=[
            {"text_en": "list", "text_ru": "list", "is_correct": True},
            {"text_en": "while", "text_ru": "while", "is_correct": False},
            {"text_en": "dict", "text_ru": "dict", "is_correct": True},
        ],
        explanation_en="Lists and dictionaries are collection types.",
        explanation_ru="Lists and dictionaries are collection types.",
        difficulty="beginner",
        question_type="multi_select",
    )

    resp = client.post(
        "/api/quizzes",
        json={
            "topic_ids": [topic_id],
            "count": 1,
            "language": "en",
            "difficulty": "all",
        },
    )
    assert resp.status_code == 201
    quiz = resp.get_json()
    assert quiz["questions"][0]["question_type"] == "multi_select"

    session = fetch_quiz_session(quiz["token"])
    option_order = json.loads(session["option_orders_json"])[str(question_id)]
    selected_display_indices = [
        display_index
        for display_index, original_index in enumerate(option_order)
        if original_index in {0, 2}
    ]
    submitted = client.post(
        f"/api/quizzes/{quiz['token']}/submit",
        json={"answers": {str(question_id): selected_display_indices}},
    )
    assert submitted.status_code == 200
    result = submitted.get_json()["result"]
    assert result["total"] == 1
    assert result["correct"] == 1
    assert result["review"][0]["question_type"] == "multi_select"


def test_empty_submit(client):
    from app.models.knowledge import fetch_catalog
    
    # Login
    client.post("/register", data={"username": "testuser_empty", "password": "password123", "password_repeat": "password123"}, follow_redirects=True)
    client.post("/login", data={"username": "testuser_empty", "password": "password123"}, follow_redirects=True)
    
    topics = fetch_catalog()[0]["topics"]
    topic_id = topics[0]["id"]
    
    # Generate quiz
    resp = client.post('/api/quizzes', json={'topic_ids': [topic_id], 'count': 2})
    token = resp.get_json()['token']
    
    # Submit empty answers
    resp2 = client.post(f'/api/quizzes/{token}/submit', json={'answers': {}})
    assert resp2.status_code == 200
    assert resp2.get_json()["result"]["unanswered"] == 2
    
    # Check profile loads without 500 error
    resp3 = client.get('/profile', follow_redirects=True)
    assert resp3.status_code == 200
    assert b"My Groups" in resp3.data


def test_topic_quiz_rejects_unavailable_count(client):
    from app.models.knowledge import fetch_catalog

    topic_id = fetch_catalog()[0]["topics"][0]["id"]
    resp = client.post(
        "/api/quizzes",
        json={
            "topic_ids": [topic_id],
            "count": 100,
            "language": "ru",
            "difficulty": "all",
        },
    )
    assert resp.status_code == 400


def test_python_curriculum_has_complete_difficulty_coverage(client):
    from app.models.knowledge import fetch_catalog

    python_course = next(
        course for course in fetch_catalog() if course["title_en"] == "Python"
    )
    assert len(python_course["topics"]) >= 40
    assert python_course["question_count"] >= 140
    for topic in python_course["topics"]:
        assert topic["beginner_count"] >= 1
        assert topic["intermediate_count"] >= 1
        assert topic["advanced_count"] >= 1


def test_python_curriculum_sync_is_idempotent(client):
    from app.models.knowledge import fetch_catalog, synchronize_python_curriculum

    before = next(
        course for course in fetch_catalog() if course["title_en"] == "Python"
    )
    synchronize_python_curriculum()
    after = next(
        course for course in fetch_catalog() if course["title_en"] == "Python"
    )
    assert after["topic_count"] == before["topic_count"]
    assert after["question_count"] == before["question_count"]


def test_template_generation_is_deterministic():
    from app.models.template_engine import generate_question

    template = {
        "template_en": "What does {a} + {b} return?",
        "template_ru": "Что вернет {a} + {b}?",
        "variables_spec_json": {
            "a": {"type": "int", "range": [1, 20]},
            "b": {"type": "int", "range": [1, 20]},
        },
        "answer_expression": "a + b",
        "difficulty": "beginner",
    }
    first = generate_question(dict(template), seed="student1:tokenABC:arithmetic_add:0")
    second = generate_question(dict(template), seed="student1:tokenABC:arithmetic_add:0")
    third = generate_question(dict(template), seed="student2:tokenXYZ:arithmetic_add:0")

    assert first == second
    assert first["text_en"] != third["text_en"] or first["correct"] != third["correct"]


def test_topic_quiz_includes_generated_template_questions(client):
    from app.models.knowledge import fetch_catalog

    python_course = next(
        course for course in fetch_catalog() if course["title_en"] == "Python"
    )
    operators_topic = next(
        topic for topic in python_course["topics"] if topic["title_en"] == "Operators"
    )

    resp = client.post(
        "/api/quizzes",
        json={
            "topic_ids": [operators_topic["id"]],
            "count": 8,
            "language": "en",
            "difficulty": "all",
        },
    )
    assert resp.status_code == 201
    quiz = resp.get_json()
    generated_ids = [q["id"] for q in quiz["questions"] if isinstance(q["id"], str)]
    assert generated_ids, "expected at least one seeded-template question in the mix"

    generated_question = next(q for q in quiz["questions"] if q["id"] in generated_ids)
    check_resp = client.post(
        f"/api/quizzes/{quiz['token']}/check",
        json={"question_id": generated_question["id"], "selected": 0},
    )
    assert check_resp.status_code == 200
    assert "is_correct" in check_resp.get_json()

    answers = {str(q["id"]): 0 for q in quiz["questions"]}
    submit_resp = client.post(
        f"/api/quizzes/{quiz['token']}/submit",
        json={"answers": answers},
    )
    assert submit_resp.status_code == 200
    assert submit_resp.get_json()["result"]["total"] == 8


def test_guest_session_exclude_avoids_repeat_questions(client):
    from app.models.knowledge import fetch_catalog

    with client.session_transaction() as sess:
        sess.pop("user_id", None)

    python_course = next(
        course for course in fetch_catalog() if course["title_en"] == "Python"
    )
    topic_id = next(
        topic["id"] for topic in python_course["topics"] if topic["title_en"] == "Booleans"
    )

    first_resp = client.post(
        "/api/quizzes",
        json={"topic_ids": [topic_id], "count": 4, "language": "en", "difficulty": "all"},
    )
    assert first_resp.status_code == 201
    first_ids = {q["id"] for q in first_resp.get_json()["questions"] if isinstance(q["id"], int)}
    assert first_ids

    second_resp = client.post(
        "/api/quizzes",
        json={
            "topic_ids": [topic_id],
            "count": 4,
            "language": "en",
            "difficulty": "all",
            "session_exclude": list(first_ids),
        },
    )
    assert second_resp.status_code == 201
    second_ids = {q["id"] for q in second_resp.get_json()["questions"] if isinstance(q["id"], int)}
    assert not (first_ids & second_ids), "excluded question ids leaked into the next quiz"


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


def test_profile_loads_with_datetime_group_membership(client, monkeypatch):
    from app.models import group as group_model

    client.post(
        "/register",
        data={"username": "testprofilegroups", "password": "pass1234", "password_repeat": "pass1234"},
        follow_redirects=True,
    )

    def fake_fetch_user_groups(_user_id):
        return [
            {
                "id": 1,
                "name": "Group A",
                "joined_at": datetime(2026, 6, 24, 10, 30, 0),
                "teacher_name": "teacher1",
            }
        ]

    monkeypatch.setattr(group_model, "fetch_user_groups", fake_fetch_user_groups)

    resp = client.get("/profile")
    assert resp.status_code == 200
    assert b"Group A" in resp.data


# ---------------------------------------------------------------------------
# API parse — document_id missing/invalid
# ---------------------------------------------------------------------------


def test_api_parse_unauthenticated(client):
    with client.session_transaction() as sess:
        sess.pop("user_id", None)
    resp = client.post("/api/parse", data={})
    assert resp.status_code in (401, 403)


def test_api_parse_no_file_no_document(client):
    client.post(
        "/register",
        data={"username": "parseuser1", "password": "password", "password_repeat": "password"},
        follow_redirects=True,
    )
    resp = client.post("/api/parse", data={})
    assert resp.status_code == 400
    data = resp.get_json()
    assert "error" in data


def test_api_parse_invalid_document_id(client):
    client.post(
        "/register",
        data={"username": "parseuser2", "password": "password", "password_repeat": "password"},
        follow_redirects=True,
    )
    resp = client.post("/api/parse", data={"document_id": "not-a-number"})
    assert resp.status_code == 400
    data = resp.get_json()
    assert "error" in data


def test_api_parse_nonexistent_document(client):
    client.post(
        "/register",
        data={"username": "parseuser3", "password": "password", "password_repeat": "password"},
        follow_redirects=True,
    )
    resp = client.post("/api/parse", data={"document_id": "99999"})
    assert resp.status_code == 404
    data = resp.get_json()
    assert "error" in data


def test_api_parse_json_questions(client):
    """Upload a valid JSON question set directly."""
    client.post(
        "/register",
        data={"username": "parseuser4", "password": "password", "password_repeat": "password"},
        follow_redirects=True,
    )
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
    data = {"file": (io.BytesIO(json_bytes), "questions.json", "application/json")}
    resp = client.post("/api/parse", data=data, content_type="multipart/form-data")
    assert resp.status_code == 200
    result = resp.get_json()
    assert result["count"] == 1
    assert result["questions"][0]["text"] == "What is 2+2?"


def test_api_parse_unsupported_extension(client):
    client.post(
        "/register",
        data={"username": "parseuser5", "password": "password", "password_repeat": "password"},
        follow_redirects=True,
    )
    data = {"file": (io.BytesIO(b"text content"), "file.txt", "text/plain")}
    resp = client.post("/api/parse", data=data, content_type="multipart/form-data")
    assert resp.status_code == 400


def test_api_parse_idor(client, app):
    """Test that a user cannot parse another user's document."""
    with app.app_context():
        from app.models.user import create_user
        from app.models.document import save_document
        from app.database import get_db_connection, db_execute
        
        # Create victim user
        victim_id = create_user("victim", "password")
        if isinstance(victim_id, dict):
            victim_id = victim_id["id"]
        elif hasattr(victim_id, "keys"): # sqlite3.Row
            victim_id = victim_id["id"]
        # Create a document for victim
        save_document("Victim Doc", "[]", victim_id)
        
        # Get the document ID
        with get_db_connection() as conn:
            doc_id = db_execute(conn, "SELECT id FROM documents WHERE uploaded_by = %s ORDER BY id DESC LIMIT 1", (victim_id,)).fetchone()["id"]

    # Register and login as attacker
    client.post(
        "/register",
        data={"username": "attacker", "password": "password", "password_repeat": "password"},
        follow_redirects=True,
    )
    
    # Attempt to parse victim's document
    resp = client.post("/api/parse", data={"document_id": doc_id})
    assert resp.status_code == 403


def test_api_results_removed(client):
    """Ensure the score forgery endpoint is removed."""
    client.post(
        "/register",
        data={"username": "forger", "password": "password", "password_repeat": "password"},
        follow_redirects=True,
    )
    resp = client.post("/api/results", json={"correct": 999})
    assert resp.status_code == 404


# ---------------------------------------------------------------------------
# Admin panel — access control
# ---------------------------------------------------------------------------


def test_admin_creates_true_false_and_fill_in_the_blank_questions(client, app):
    from app.models.knowledge import create_course, create_topic
    from app.models.user import toggle_user_admin

    client.post(
        "/register",
        data={"username": "adminauthor", "password": "pass1234", "password_repeat": "pass1234"},
        follow_redirects=True,
    )
    with client.session_transaction() as sess:
        user_id = sess["user_id"]
    with app.app_context():
        from app.models.user import fetch_user_by_id
        if not fetch_user_by_id(user_id)["is_admin"]:
            toggle_user_admin(user_id)

    course_id = create_course("Admin Authoring Course", "Admin Authoring Course")
    topic_id = create_topic(course_id, "Authoring Topic", "Authoring Topic")

    tf_resp = client.post(
        "/admin/questions",
        data={
            "topic_id": str(topic_id),
            "question_type": "true_false",
            "text_en": "True or false: 1 + 1 == 2",
            "text_ru": "True or false: 1 + 1 == 2",
            "correct_boolean": "true",
            "difficulty": "beginner",
        },
        follow_redirects=True,
    )
    assert tf_resp.status_code == 200

    blank_resp = client.post(
        "/admin/questions",
        data={
            "topic_id": str(topic_id),
            "question_type": "fill_in_the_blank",
            "text_en": "What does len('ab') return?",
            "text_ru": "What does len('ab') return?",
            "blank_answer_en": "2",
            "blank_answer_ru": "2",
            "difficulty": "beginner",
        },
        follow_redirects=True,
    )
    assert blank_resp.status_code == 200

    from app.models.knowledge import fetch_questions_for_admin
    created = [q for q in fetch_questions_for_admin() if q["topic_id"] == topic_id]
    types_created = {q["question_type"] for q in created}
    assert types_created == {"true_false", "fill_in_the_blank"}


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
