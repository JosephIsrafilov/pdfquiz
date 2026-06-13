import io
import json
import os
import re
import sqlite3
import tempfile
import xml.etree.ElementTree as ET
from functools import wraps
from html import unescape
from typing import Dict, List, Optional, Tuple
from zipfile import BadZipFile, ZipFile

import pdfplumber
try:
    import psycopg
    from psycopg.rows import dict_row
except ImportError:
    psycopg = None
    dict_row = None
from flask import (
    Flask,
    abort,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import RequestEntityTooLarge

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 25 * 1024 * 1024
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")


@app.after_request
def add_ngrok_skip_header(response):
    response.headers["ngrok-skip-browser-warning"] = "true"
    return response


@app.errorhandler(RequestEntityTooLarge)
def handle_file_too_large(_error):
    return jsonify({"error": "Файл слишком большой. Максимум 25 МБ."}), 413


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.environ.get("DB_PATH", os.path.join(BASE_DIR, "app.db"))
DATABASE_URL = os.environ.get("DATABASE_URL")
USING_POSTGRES = bool(DATABASE_URL)

db_dir = os.path.dirname(DB_PATH)
if db_dir:
    os.makedirs(db_dir, exist_ok=True)

QUIZ_SIZE = 50
MIN_RANGE = QUIZ_SIZE


def get_db_connection():
    if USING_POSTGRES:
        if psycopg is None or dict_row is None:
            raise RuntimeError("psycopg is required when DATABASE_URL is set")
        return psycopg.connect(DATABASE_URL, row_factory=dict_row)

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def db_query(query: str) -> str:
    if USING_POSTGRES:
        return query
    return query.replace("%s", "?")


def db_execute(connection, query: str, params=()):
    return connection.execute(db_query(query), params)


def get_first_column(row) -> Optional[object]:
    if row is None:
        return None
    if isinstance(row, dict):
        return next(iter(row.values()))
    return row[0]


def init_db() -> None:
    with get_db_connection() as connection:
        if USING_POSTGRES:
            statements = [
                """
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    is_admin BOOLEAN NOT NULL DEFAULT FALSE,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS documents (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    original_filename TEXT,
                    question_count INTEGER NOT NULL DEFAULT 0,
                    questions_json TEXT NOT NULL,
                    uploaded_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS results (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    document_id INTEGER REFERENCES documents(id) ON DELETE SET NULL,
                    source_label TEXT NOT NULL,
                    total_questions INTEGER NOT NULL,
                    quiz_size INTEGER NOT NULL,
                    graded INTEGER NOT NULL,
                    correct INTEGER NOT NULL,
                    unanswered INTEGER NOT NULL,
                    missing_answer_key INTEGER NOT NULL,
                    mistake_numbers_json TEXT NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """,
            ]
            for statement in statements:
                db_execute(connection, statement)
            db_execute(
                connection,
                "ALTER TABLE results ADD COLUMN IF NOT EXISTS attempt_json TEXT",
            )
        else:
            statements = [
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    is_admin INTEGER NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    original_filename TEXT,
                    question_count INTEGER NOT NULL DEFAULT 0,
                    questions_json TEXT NOT NULL,
                    uploaded_by INTEGER,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(uploaded_by) REFERENCES users(id)
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    document_id INTEGER,
                    source_label TEXT NOT NULL,
                    total_questions INTEGER NOT NULL,
                    quiz_size INTEGER NOT NULL,
                    graded INTEGER NOT NULL,
                    correct INTEGER NOT NULL,
                    unanswered INTEGER NOT NULL,
                    missing_answer_key INTEGER NOT NULL,
                    mistake_numbers_json TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(id),
                    FOREIGN KEY(document_id) REFERENCES documents(id)
                )
                """,
            ]
            for statement in statements:
                db_execute(connection, statement)

            result_columns = {
                row["name"]
                for row in db_execute(connection, "PRAGMA table_info(results)").fetchall()
            }
            if "attempt_json" not in result_columns:
                db_execute(connection, "ALTER TABLE results ADD COLUMN attempt_json TEXT")
        connection.commit()


def fetch_user_by_id(user_id: Optional[int]):
    if not user_id:
        return None
    with get_db_connection() as connection:
        return db_execute(
            connection,
            "SELECT id, username, is_admin, created_at FROM users WHERE id = %s",
            (user_id,),
        ).fetchone()


def fetch_user_by_username(username: str):
    with get_db_connection() as connection:
        return db_execute(
            connection,
            "SELECT * FROM users WHERE lower(username) = lower(%s)",
            (username.strip(),),
        ).fetchone()


def get_current_user():
    return fetch_user_by_id(session.get("user_id"))


def serialize_user(row: Optional[sqlite3.Row]) -> Optional[Dict]:
    if row is None:
        return None
    return {
        "id": row["id"],
        "username": row["username"],
        "is_admin": bool(row["is_admin"]),
        "created_at": row["created_at"],
    }


def login_user(user_id: int) -> None:
    session["user_id"] = user_id


def logout_user() -> None:
    session.pop("user_id", None)


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if get_current_user() is None:
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)

    return wrapped


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        user = get_current_user()
        if user is None:
            return redirect(url_for("login", next=request.path))
        if not user["is_admin"]:
            abort(403)
        return view(*args, **kwargs)

    return wrapped


def create_user(username: str, password: str):
    normalized_username = username.strip()
    with get_db_connection() as connection:
        user_count = get_first_column(
            db_execute(connection, "SELECT COUNT(*) FROM users").fetchone()
        )
        is_admin = user_count == 0
        if USING_POSTGRES:
            user = db_execute(
                connection,
                """
                INSERT INTO users (username, password_hash, is_admin)
                VALUES (%s, %s, %s)
                RETURNING id, username, is_admin, created_at
                """,
                (normalized_username, generate_password_hash(password), is_admin),
            ).fetchone()
            connection.commit()
            return user

        cursor = db_execute(
            connection,
            """
            INSERT INTO users (username, password_hash, is_admin)
            VALUES (%s, %s, %s)
            """,
            (normalized_username, generate_password_hash(password), int(is_admin)),
        )
        connection.commit()
        return db_execute(
            connection,
            "SELECT id, username, is_admin, created_at FROM users WHERE id = %s",
            (cursor.lastrowid,),
        ).fetchone()


def fetch_documents() -> List[Dict]:
    with get_db_connection() as connection:
        return db_execute(
            connection,
            """
            SELECT documents.id, documents.title, documents.original_filename,
                   documents.question_count, documents.created_at,
                   users.username AS uploader_name
            FROM documents
            LEFT JOIN users ON users.id = documents.uploaded_by
            ORDER BY documents.created_at DESC, documents.id DESC
            """
        ).fetchall()


def fetch_document(document_id: int):
    with get_db_connection() as connection:
        return db_execute(
            connection,
            """
            SELECT id, title, original_filename, question_count, questions_json, created_at
            FROM documents
            WHERE id = %s
            """,
            (document_id,),
        ).fetchone()


def serialize_document(row: sqlite3.Row) -> Dict:
    return {
        "id": row["id"],
        "title": row["title"],
        "original_filename": row["original_filename"],
        "question_count": row["question_count"],
        "created_at": row["created_at"],
        "uploader_name": row["uploader_name"] if "uploader_name" in row.keys() else None,
    }


def save_document(
    title: str,
    original_filename: str,
    questions: List[Dict],
    uploaded_by: Optional[int],
) -> None:
    with get_db_connection() as connection:
        db_execute(
            connection,
            """
            INSERT INTO documents (title, original_filename, question_count, questions_json, uploaded_by)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                title.strip(),
                original_filename,
                len(questions),
                json.dumps(questions, ensure_ascii=False),
                uploaded_by,
            ),
        )
        connection.commit()


def delete_document(document_id: int) -> None:
    with get_db_connection() as connection:
        db_execute(connection, "DELETE FROM results WHERE document_id = %s", (document_id,))
        db_execute(connection, "DELETE FROM documents WHERE id = %s", (document_id,))
        connection.commit()


def fetch_results_for_user(user_id: int, limit: int = 20) -> List[Dict]:
    with get_db_connection() as connection:
        return db_execute(
            connection,
            """
            SELECT id, source_label, total_questions, quiz_size, graded, correct,
                   unanswered, missing_answer_key, mistake_numbers_json, created_at,
                   attempt_json
            FROM results
            WHERE user_id = %s
            ORDER BY created_at DESC, id DESC
            LIMIT %s
            """,
            (user_id, limit),
        ).fetchall()


def fetch_result_for_user(user_id: int, result_id: int):
    with get_db_connection() as connection:
        return db_execute(
            connection,
            """
            SELECT id, user_id, document_id, source_label, total_questions, quiz_size,
                   graded, correct, unanswered, missing_answer_key, mistake_numbers_json,
                   created_at, attempt_json
            FROM results
            WHERE id = %s AND user_id = %s
            """,
            (result_id, user_id),
        ).fetchone()


def save_result(
    *,
    user_id: int,
    document_id: Optional[int],
    source_label: str,
    total_questions: int,
    quiz_size: int,
    graded: int,
    correct: int,
    unanswered: int,
    missing_answer_key: int,
    mistake_numbers: List[int],
    attempt_payload: Optional[Dict],
) -> None:
    with get_db_connection() as connection:
        db_execute(
            connection,
            """
            INSERT INTO results (
                user_id, document_id, source_label, total_questions, quiz_size,
                graded, correct, unanswered, missing_answer_key, mistake_numbers_json,
                attempt_json
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                user_id,
                document_id,
                source_label,
                total_questions,
                quiz_size,
                graded,
                correct,
                unanswered,
                missing_answer_key,
                json.dumps(mistake_numbers),
                json.dumps(attempt_payload, ensure_ascii=False)
                if attempt_payload is not None
                else None,
            ),
        )
        connection.commit()


def serialize_result(row) -> Dict:
    return {
        "id": row["id"],
        "source_label": row["source_label"],
        "total_questions": row["total_questions"],
        "quiz_size": row["quiz_size"],
        "graded": row["graded"],
        "correct": row["correct"],
        "unanswered": row["unanswered"],
        "missing_answer_key": row["missing_answer_key"],
        "mistake_numbers": json.loads(row["mistake_numbers_json"]),
        "created_at": row["created_at"],
        "attempt_available": bool(row["attempt_json"]),
    }


def build_attempt_review(row) -> Optional[List[Dict]]:
    if not row["attempt_json"]:
        return None

    attempt = json.loads(row["attempt_json"])
    quiz = attempt.get("quiz", [])
    answers = attempt.get("answers", {})
    review: List[Dict] = []

    for index, question in enumerate(quiz):
        selected_index = answers.get(str(index))
        if selected_index is None:
            selected_index = answers.get(index)
        selected_index = int(selected_index) if selected_index is not None else None

        option_rows = []
        correct_indices = []
        for opt_index, option in enumerate(question.get("options", [])):
            is_correct = bool(option.get("is_correct"))
            if is_correct:
                correct_indices.append(opt_index)
            option_rows.append(
                {
                    "label": chr(65 + opt_index),
                    "text": option.get("text", ""),
                    "is_correct": is_correct,
                    "is_selected": selected_index == opt_index,
                    "is_wrong_selected": selected_index == opt_index and not is_correct,
                }
            )

        review.append(
            {
                "index": index + 1,
                "number": question.get("number"),
                "text": question.get("text", ""),
                "options": option_rows,
                "selected_index": selected_index,
                "is_unanswered": selected_index is None,
                "has_answer_key": bool(correct_indices),
                "is_correct": selected_index in correct_indices if correct_indices else False,
            }
        )

    return review


def normalize_imported_questions(questions: object) -> List[Dict]:
    if not isinstance(questions, list):
        raise ValueError("JSON должен содержать массив вопросов.")

    normalized: List[Dict] = []
    for index, question in enumerate(questions, start=1):
        if not isinstance(question, dict):
            raise ValueError(f"Вопрос {index}: ожидается объект.")

        text = normalize_space(str(question.get("text", "")))
        if not text:
            raise ValueError(f"Вопрос {index}: отсутствует текст вопроса.")

        raw_options = question.get("options")
        if not isinstance(raw_options, list) or len(raw_options) < 2:
            raise ValueError(f"Вопрос {index}: нужно минимум 2 варианта ответа.")

        options: List[Dict] = []
        for option_index, option in enumerate(raw_options, start=1):
            if not isinstance(option, dict):
                raise ValueError(
                    f"Вопрос {index}, вариант {option_index}: ожидается объект."
                )
            option_text = normalize_space(str(option.get("text", "")))
            if not option_text:
                raise ValueError(
                    f"Вопрос {index}, вариант {option_index}: пустой текст."
                )
            options.append(
                {
                    "text": option_text,
                    "is_correct": bool(option.get("is_correct")),
                }
            )

        normalized.append(
            {
                "number": question.get("number"),
                "text": text,
                "options": options,
                "answer_hint": question.get("answer_hint"),
            }
        )

    return normalized


def parse_uploaded_questions(filename: str, file_bytes: bytes) -> List[Dict]:
    lowered = filename.lower()
    if lowered.endswith(".pdf"):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name
        try:
            return parse_pdf_questions(tmp_path)
        finally:
            os.unlink(tmp_path)
    if lowered.endswith(".docx"):
        return parse_docx_questions(extract_docx_paragraphs(file_bytes))
    if lowered.endswith(".json"):
        payload = json.loads(file_bytes.decode("utf-8"))
        return normalize_imported_questions(payload)
    raise ValueError("Поддерживаются только PDF, DOCX и JSON.")


def parse_uploaded_file(filename: str, file_storage) -> List[Dict]:
    """Stream file to disk for PDF to avoid double-buffering in RAM."""
    lowered = filename.lower()
    if lowered.endswith(".pdf"):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            file_storage.save(tmp)
            tmp_path = tmp.name
        try:
            return parse_pdf_questions(tmp_path)
        finally:
            os.unlink(tmp_path)
    file_bytes = file_storage.read()
    if lowered.endswith(".docx"):
        return parse_docx_questions(extract_docx_paragraphs(file_bytes))
    if lowered.endswith(".json"):
        payload = json.loads(file_bytes.decode("utf-8"))
        return normalize_imported_questions(payload)
    raise ValueError("Поддерживаются только PDF, DOCX и JSON.")


def fetch_users() -> List[Dict]:
    with get_db_connection() as connection:
        return db_execute(
            connection,
            """
            SELECT id, username, is_admin, created_at
            FROM users
            ORDER BY created_at ASC, id ASC
            """
        ).fetchall()


def toggle_user_admin(user_id: int) -> None:
    with get_db_connection() as connection:
        db_execute(
            connection,
            """
            UPDATE users
            SET is_admin = NOT COALESCE(is_admin, FALSE)
            WHERE id = %s
            """,
            (user_id,),
        )
        connection.commit()


def delete_user(user_id: int) -> None:
    with get_db_connection() as connection:
        db_execute(connection, "DELETE FROM results WHERE user_id = %s", (user_id,))
        db_execute(connection, "DELETE FROM users WHERE id = %s", (user_id,))
        connection.commit()


init_db()

from parsers.common import parse_questions
from parsers.docx_parser import parse_docx_questions, extract_docx_paragraphs
from parsers.pdf_parser import parse_pdf_questions

@app.route("/")
def index():
    current_user = get_current_user()
    documents = [serialize_document(row) for row in fetch_documents()]
    return render_template(
        "index.html",
        current_user=serialize_user(current_user),
        documents=documents,
    )


@app.route("/profile")
@login_required
def profile():
    current_user = get_current_user()
    results = [
        serialize_result(row)
        for row in fetch_results_for_user(current_user["id"], limit=100)
    ]
    return render_template(
        "profile.html",
        current_user=serialize_user(current_user),
        results=results,
    )


@app.route("/profile/results/<int:result_id>")
@login_required
def profile_result_detail(result_id: int):
    current_user = get_current_user()
    row = fetch_result_for_user(current_user["id"], result_id)
    if row is None:
        abort(404)

    result = serialize_result(row)
    review = build_attempt_review(row)
    return render_template(
        "result_detail.html",
        current_user=serialize_user(current_user),
        result=result,
        review=review,
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    next_url = request.values.get("next") or url_for("index")
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = fetch_user_by_username(username)
        if user is None or not check_password_hash(user["password_hash"], password):
            error = "Неверный логин или пароль."
        else:
            login_user(user["id"])
            return redirect(next_url)
    return render_template("login.html", error=error, next_url=next_url)


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    next_url = request.values.get("next") or url_for("index")
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        password_repeat = request.form.get("password_repeat", "")

        if len(username) < 3:
            error = "Логин должен содержать минимум 3 символа."
        elif len(password) < 6:
            error = "Пароль должен содержать минимум 6 символов."
        elif password != password_repeat:
            error = "Пароли не совпадают."
        elif fetch_user_by_username(username) is not None:
            error = "Пользователь с таким логином уже существует."
        else:
            user = create_user(username, password)
            login_user(user["id"])
            return redirect(next_url)

    return render_template("register.html", error=error, next_url=next_url)


@app.route("/logout", methods=["POST"])
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/admin")
@admin_required
def admin_panel():
    current_user = get_current_user()
    documents = [serialize_document(row) for row in fetch_documents()]
    users = [serialize_user(row) for row in fetch_users()]
    return render_template(
        "admin.html",
        current_user=serialize_user(current_user),
        documents=documents,
        users=users,
        error=request.args.get("error"),
        success=request.args.get("success"),
    )


@app.route("/admin/documents", methods=["POST"])
@admin_required
def admin_upload_document():
    file = request.files.get("file")
    title = (request.form.get("title") or "").strip()
    if not file or not file.filename:
        return redirect(url_for("admin_panel", error="Выберите PDF, DOCX или JSON файл."))
    if not title:
        title = os.path.splitext(file.filename)[0]

    filename = file.filename.lower()
    if not filename.endswith((".pdf", ".docx", ".json")):
        return redirect(url_for("admin_panel", error="Поддерживаются только PDF, DOCX и JSON."))

    try:
        questions = parse_uploaded_file(filename, file)
    except ValueError as error:
        return redirect(url_for("admin_panel", error=str(error)))
    except Exception:
        return redirect(url_for("admin_panel", error="Не удалось обработать файл."))

    if not questions:
        return redirect(url_for("admin_panel", error="В файле не удалось распознать вопросы."))

    current_user = get_current_user()
    save_document(title, file.filename, questions, current_user["id"] if current_user else None)
    return redirect(url_for("admin_panel", success="Документ успешно загружен."))


@app.route("/admin/documents/<int:document_id>/delete", methods=["POST"])
@admin_required
def admin_delete_document(document_id: int):
    delete_document(document_id)
    return redirect(url_for("admin_panel", success="Документ удален."))


@app.route("/admin/users/<int:user_id>/toggle-admin", methods=["POST"])
@admin_required
def admin_toggle_user(user_id: int):
    current_user = get_current_user()
    if current_user and current_user["id"] == user_id:
        return redirect(url_for("admin_panel", error="Нельзя менять роль самому себе."))
    toggle_user_admin(user_id)
    return redirect(url_for("admin_panel", success="Роль пользователя обновлена."))


@app.route("/admin/users/<int:user_id>/delete", methods=["POST"])
@admin_required
def admin_delete_user(user_id: int):
    current_user = get_current_user()
    if current_user and current_user["id"] == user_id:
        return redirect(url_for("admin_panel", error="Нельзя удалить самого себя."))
    delete_user(user_id)
    return redirect(url_for("admin_panel", success="Пользователь удален."))


@app.route("/api/parse", methods=["POST"])
def parse_document():
    document_id_raw = request.form.get("document_id", "").strip()
    source_label = "Загруженный файл"
    document_id = None

    if document_id_raw:
        try:
            document_id = int(document_id_raw)
        except ValueError:
            return jsonify({"error": "Некорректный документ"}), 400

        document = fetch_document(document_id)
        if document is None:
            return jsonify({"error": "Документ не найден"}), 404
        questions = json.loads(document["questions_json"])
        source_label = document["title"]
    else:
        if "file" not in request.files:
            return jsonify({"error": "Файл не найден"}), 400

        file = request.files["file"]
        if not file or not file.filename:
            return jsonify({"error": "Файл не выбран"}), 400

        filename = file.filename.lower()
        if not filename.endswith((".pdf", ".docx", ".json")):
            return jsonify({"error": "Поддерживаются только PDF, DOCX и JSON"}), 400

        try:
            questions = parse_uploaded_file(filename, file)
            source_label = file.filename
        except ValueError as error:
            return jsonify({"error": str(error)}), 400
        except BadZipFile:
            return jsonify({"error": "DOCX файл поврежден или имеет неверный формат"}), 400
        except KeyError:
            return jsonify({"error": "Не удалось прочитать структуру DOCX"}), 400
        except Exception:
            return jsonify({"error": "Не удалось прочитать файл"}), 500

    if not questions:
        return jsonify({"error": "Не удалось распознать вопросы"}), 400

    return jsonify(
        {
            "count": len(questions),
            "questions": questions,
            "document_id": document_id,
            "source_label": source_label,
        }
    )


@app.route("/api/results", methods=["POST"])
@login_required
def save_quiz_result():
    payload = request.get_json(silent=True) or {}
    required_keys = {
        "source_label",
        "total_questions",
        "quiz_size",
        "graded",
        "correct",
        "unanswered",
        "missing_answer_key",
        "mistake_numbers",
        "attempt",
    }
    if not required_keys.issubset(payload.keys()):
        return jsonify({"error": "Недостаточно данных для сохранения результата."}), 400

    current_user = get_current_user()
    save_result(
        user_id=current_user["id"],
        document_id=payload.get("document_id"),
        source_label=str(payload["source_label"]),
        total_questions=int(payload["total_questions"]),
        quiz_size=int(payload["quiz_size"]),
        graded=int(payload["graded"]),
        correct=int(payload["correct"]),
        unanswered=int(payload["unanswered"]),
        missing_answer_key=int(payload["missing_answer_key"]),
        mistake_numbers=[int(value) for value in payload.get("mistake_numbers", [])],
        attempt_payload=payload.get("attempt"),
    )

    latest = fetch_results_for_user(current_user["id"], limit=1)
    return jsonify({"ok": True, "result": serialize_result(latest[0]) if latest else None})


if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT") or os.environ.get("SERVER_PORT") or "5000")
    debug = os.environ.get("DEBUG", "0").lower() in ("1", "true", "yes")
    app.run(host=host, port=port, debug=debug)
