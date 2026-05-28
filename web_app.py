import io
import json
import os
import re
import sqlite3
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
        return parse_pdf_questions(file_bytes)
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

QUESTION_PATTERNS = [
    re.compile(r"^\s*(\d{1,4})[\.\)\-]\s*(.*)$"),
    re.compile(r"^\s*(\d{1,4})\s+(.+)$"),
    re.compile(r"^\s*(\d{1,4})\s*$"),
    re.compile(
        r"^\s*(?:Вопрос|Question)\s*(\d{1,4})[\.:\-\)]?\s*(.*)$",
        re.IGNORECASE,
    ),
]

OPTION_PATTERN = re.compile(r"^\s*([A-ZА-Я]|\d{1,2})[\.\)\:\-]\s+(.*)$")
ANSWER_LINE_PATTERN = re.compile(
    r"^(?:Ответ|Answer|Correct(?: answer)?|Правильный ответ)\s*[:\-]\s*(.+)$",
    re.IGNORECASE,
)
QUESTION_SCORE_PATTERN = re.compile(r"^\(\s*\d+\s*т\s*\)\s*", re.IGNORECASE)
DOCX_NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
DOCX_NUMBERED_FORMATS = {"decimal", "lowerLetter", "upperLetter", "lowerRoman", "upperRoman"}

BULLET_CHARS = "•·∙‣◦◉○●▪▫■\uf0b7"
CHECK_CHARS = "✓✔√☑✅🗸"
OPTION_PREFIX_CHARS = BULLET_CHARS + CHECK_CHARS


def make_char_class(chars: str) -> str:
    return "".join(re.escape(ch) for ch in chars)


_MARKER_CLASS = make_char_class(OPTION_PREFIX_CHARS)
OPTION_BULLET_PATTERN = re.compile(rf"^\s*[{_MARKER_CLASS}]\s*(.+)$")
BULLET_SPLIT_PATTERN = re.compile(rf"(?=[{_MARKER_CLASS}])")


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\u00a0", " ")).strip()


def strip_question_leading_noise(text: str) -> str:
    cleaned = normalize_space(text)
    previous = None
    while cleaned != previous:
        previous = cleaned
        if cleaned.startswith("+"):
            cleaned = normalize_space(cleaned[1:])
        cleaned = QUESTION_SCORE_PATTERN.sub("", cleaned)
        cleaned = normalize_space(cleaned)
    return cleaned


def strip_correct_markers(text: str) -> Tuple[str, bool]:
    cleaned = text.strip()
    is_correct = False

    if re.search(r"\((?:верно|правильно|correct)\)", cleaned, re.IGNORECASE):
        is_correct = True
        cleaned = re.sub(
            r"\((?:верно|правильно|correct)\)",
            "",
            cleaned,
            flags=re.IGNORECASE,
        ).strip()

    if re.search(r"\[\s*[xX]\s*\]", cleaned):
        is_correct = True
        cleaned = re.sub(r"\[\s*[xX]\s*\]", "", cleaned).strip()

    if cleaned.endswith("*"):
        is_correct = True
        cleaned = cleaned.rstrip("*").strip()

    if any(cleaned.endswith(ch) for ch in CHECK_CHARS):
        is_correct = True
        cleaned = cleaned.rstrip(CHECK_CHARS).strip()

    return cleaned, is_correct


def clean_option_text(text: str) -> Tuple[str, bool]:
    has_check = any(ch in text for ch in CHECK_CHARS)
    cleaned = text
    for ch in CHECK_CHARS:
        cleaned = cleaned.replace(ch, " ")
    for ch in BULLET_CHARS:
        cleaned = cleaned.replace(ch, " ")
    cleaned = normalize_space(cleaned)
    cleaned, marker_correct = strip_correct_markers(cleaned)
    return cleaned, has_check or marker_correct


def first_marker_index(line: str) -> int:
    indices = [line.find(ch) for ch in OPTION_PREFIX_CHARS if line.find(ch) != -1]
    return min(indices) if indices else -1


def expand_bullet_lines(lines: List[str]) -> List[str]:
    expanded: List[str] = []
    marker_chars = OPTION_PREFIX_CHARS
    i = 0

    def ends_sentence(text: str) -> bool:
        return text.rstrip().endswith((".", ";", ":", "!", "?"))

    while i < len(lines):
        line = lines[i]
        if not line:
            i += 1
            continue

        stripped = line.strip()
        next_line = lines[i + 1] if i + 1 < len(lines) else ""
        next_stripped = next_line.strip()
        next_next_line = lines[i + 2] if i + 2 < len(lines) else ""
        next_next_stripped = next_next_line.strip()
        if (
            stripped
            and next_stripped
            and len(next_stripped) == 1
            and next_stripped in marker_chars
            and next_next_stripped
            and not ends_sentence(stripped)
        ):
            combined = f"{next_stripped} {stripped} {next_next_stripped}"
            line = combined
            i += 2
        else:
            next_match = (
                OPTION_BULLET_PATTERN.match(next_line.strip()) if next_line else None
            )
            if (
                not OPTION_BULLET_PATTERN.match(stripped)
                and next_match
                and stripped
                and not ends_sentence(stripped)
            ):
                marker = next_line.strip()[0]
                combined = f"{marker} {stripped} {next_match.group(1).strip()}"
                line = combined
                i += 1

        stripped = line.strip()
        if len(stripped) == 1 and stripped in marker_chars:
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines):
                line = f"{stripped} {lines[j].lstrip()}"
                i = j
            else:
                i += 1
                continue

        marker_count = sum(line.count(ch) for ch in marker_chars)
        if marker_count >= 2:
            parts = [part.strip() for part in BULLET_SPLIT_PATTERN.split(line)]
            for part in parts:
                if part:
                    expanded.append(part)
        elif marker_count == 1 and not OPTION_BULLET_PATTERN.match(line):
            first_idx = first_marker_index(line)
            if first_idx > 0:
                before = line[:first_idx].rstrip()
                after = line[first_idx:].lstrip()
                if before:
                    expanded.append(before)
                if after:
                    expanded.append(after)
                continue
            expanded.append(line)
        else:
            expanded.append(line)
        i += 1
    return expanded


def leading_ws_count(line: str) -> int:
    return len(line) - len(line.lstrip(" \t\u00a0"))


def is_decimal_line(line: str) -> bool:
    if re.match(r"^\s*(\d{1,4})\.\1(?:[\.\)\-]|\s)", line):
        return False
    return bool(re.match(r"^\s*\d{1,4}\.\d", line))


def is_option_line(line: str) -> bool:
    return bool(OPTION_PATTERN.match(line) or OPTION_BULLET_PATTERN.match(line))


def is_answer_line(line: str) -> bool:
    return bool(ANSWER_LINE_PATTERN.match(line.strip()))


def is_page_marker_line(line: str) -> bool:
    return bool(re.match(r"^\s*\d+\s*/\s*\d+\s*$", line))


def match_question_line(
    line: str, min_indent: int, last_number: Optional[int]
) -> Optional[Tuple[int, str]]:
    cleaned_line = line
    stripped = line.strip()
    if stripped and stripped[0] in OPTION_PREFIX_CHARS:
        cleaned_line = stripped[1:].lstrip()
    cleaned_line = strip_question_leading_noise(cleaned_line)

    if is_decimal_line(cleaned_line):
        return None

    if leading_ws_count(line) > min_indent + 1:
        return None

    for pattern in QUESTION_PATTERNS:
        match = pattern.match(cleaned_line)
        if not match:
            continue

        number = int(match.group(1)) if match.group(1) else None
        if number is None:
            return None

        if last_number is not None:
            if number % 10 == 0 and number // 10 == last_number + 1:
                number = number // 10
            if number <= last_number:
                return None
            if number > last_number + 5:
                return None

        if match.lastindex and match.lastindex >= 2:
            rest = (match.group(2) or "").strip()
        else:
            rest = line[match.end() :].strip()

        duplicate_prefix = re.compile(rf"^{number}[\.\)\-]\s*")
        while duplicate_prefix.match(rest):
            rest = duplicate_prefix.sub("", rest, count=1).strip()
        rest = strip_question_leading_noise(rest)

        if rest and rest[0].isdigit() and len(rest) > 1 and rest[1].isdigit():
            return None

        return number, rest

    return None


def split_into_question_blocks(lines: List[str]) -> List[Dict]:
    blocks: List[Dict] = []
    current: Optional[Dict] = None
    last_number: Optional[int] = None

    non_empty_lines = [line for line in lines if line.strip()]
    if not non_empty_lines:
        return []
    min_indent = min(leading_ws_count(line) for line in non_empty_lines)

    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue

        match = match_question_line(line, min_indent, last_number)
        if match:
            number, rest = match
            if current and not rest:
                option_indices = [
                    idx for idx, value in enumerate(current["lines"]) if is_option_line(value)
                ]
                if option_indices:
                    last_option_idx = option_indices[-1]
                    trailing = current["lines"][last_option_idx + 1 :]
                    if trailing and all(
                        not is_option_line(value) and not is_answer_line(value)
                        for value in trailing
                    ):
                        if all(
                            leading_ws_count(value) <= min_indent + 1
                            for value in trailing
                        ):
                            current["lines"] = current["lines"][: last_option_idx + 1]
                            blocks.append(current)
                            current = {"number": number, "lines": trailing}
                            last_number = number
                            i += 1
                            continue
            if current:
                blocks.append(current)
            current = {"number": number, "lines": [rest] if rest else []}
            last_number = number
            i += 1
            continue

        if current:
            has_options = any(is_option_line(value) for value in current["lines"])
            if has_options and not is_option_line(line) and not is_answer_line(line):
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                if j < len(lines):
                    next_match = match_question_line(lines[j], min_indent, last_number)
                    if next_match:
                        number, rest = next_match
                        blocks.append(current)
                        current = {"number": number, "lines": [line]}
                        if rest:
                            current["lines"].append(rest)
                        last_number = number
                        i = j + 1
                        continue
            current["lines"].append(line)
        i += 1

    if current:
        blocks.append(current)

    return blocks


def parse_question_block(block: Dict) -> Dict:
    question_lines: List[str] = []
    options: List[Dict] = []
    current_option: Optional[Dict] = None
    answer_hint: Optional[str] = None
    base_indent = None

    for raw_line in block["lines"]:
        line_clean = raw_line.strip()
        if not line_clean:
            continue
        if ANSWER_LINE_PATTERN.match(line_clean):
            continue
        if OPTION_PATTERN.match(raw_line) or OPTION_BULLET_PATTERN.match(raw_line):
            continue
        indent = leading_ws_count(raw_line)
        if base_indent is None or indent < base_indent:
            base_indent = indent

    if base_indent is None:
        base_indent = 0

    def option_looks_complete(text: str) -> bool:
        return text.rstrip().endswith((";", ".", ":", "!", "?"))

    def line_has_marker(text: str) -> bool:
        return any(ch in text for ch in OPTION_PREFIX_CHARS)

    def looks_like_definition_head(text: str) -> bool:
        lower = text.lower()
        return text.rstrip().endswith(":") or "это" in lower

    def looks_like_stem_boundary(text: str) -> bool:
        stripped = text.rstrip()
        return (
            "?" in stripped
            or stripped.endswith(":")
            or stripped.endswith(("...", "…", "….", "…..", "."))
        )

    def split_bare_options(
        lines: List[str], existing_option_count: int = 0
    ) -> Optional[Tuple[List[str], List[str]]]:
        filtered = [
            normalize_space(value)
            for value in lines
            if normalize_space(value) and not is_page_marker_line(value)
        ]
        if len(filtered) < 3:
            return None

        best_index = None
        best_score = -1
        for idx in range(len(filtered) - 1):
            trailing_count = len(filtered) - idx - 1 + existing_option_count
            if trailing_count < 2:
                continue

            score = 0
            if looks_like_stem_boundary(filtered[idx]):
                score += 3
            if idx == 0 and len(filtered) - 1 >= 4:
                score += 1

            if score > best_score:
                best_index = idx
                best_score = score

        if best_index is None or best_score < 1:
            return None

        return filtered[: best_index + 1], filtered[best_index + 1 :]

    def should_treat_as_question_intro(line: str, line_index: int) -> bool:
        opt_match = OPTION_PATTERN.match(line)
        if not opt_match:
            return False

        marker = opt_match.group(1)
        if not marker or len(marker) != 1:
            return False

        remaining = [
            value
            for value in block["lines"][line_index + 1 :]
            if value.strip() and not is_answer_line(value)
        ]
        if not remaining or any(is_option_line(value) for value in remaining):
            return False

        intro_text = opt_match.group(2).strip()
        if not intro_text:
            return False

        # PDF text layers sometimes split author initials like "К. Маркс" and
        # "О. Конт" so the line looks like an option marker even though it is
        # the beginning of the question.
        return intro_text[0].isupper()

    def should_ignore_single_letter_option_marker(line: str, line_index: int) -> bool:
        opt_match = OPTION_PATTERN.match(line)
        if not opt_match:
            return False

        marker = opt_match.group(1)
        if not marker or len(marker) != 1 or marker.isdigit():
            return False

        remaining = [
            value
            for value in block["lines"][line_index + 1 :]
            if value.strip()
            and not is_answer_line(value)
            and not is_page_marker_line(value)
        ]
        if not remaining or any(is_option_line(value) for value in remaining):
            return False

        text = opt_match.group(2).strip()
        return bool(text) and text[0].isupper()

    for line_index, raw_line in enumerate(block["lines"]):
        line = raw_line.rstrip()
        line_stripped = line.strip()
        if not line_stripped:
            continue
        if is_page_marker_line(line_stripped):
            continue

        answer_match = ANSWER_LINE_PATTERN.match(line_stripped)
        if answer_match:
            answer_hint = answer_match.group(1).strip()
            continue

        opt_match = OPTION_PATTERN.match(line)
        bullet_match = None
        if not opt_match:
            bullet_match = OPTION_BULLET_PATTERN.match(line)
        elif not question_lines and not current_option and should_treat_as_question_intro(
            line, line_index
        ):
            opt_match = None
        elif not current_option and should_ignore_single_letter_option_marker(
            line, line_index
        ):
            opt_match = None

        if opt_match or bullet_match:
            if current_option:
                options.append(current_option)
            if opt_match:
                text = opt_match.group(2).strip()
                cleaned_text, is_correct = clean_option_text(text)
            else:
                prefix = line_stripped[0]
                text = bullet_match.group(1).strip()
                cleaned_text, is_correct = clean_option_text(text)
                if prefix in CHECK_CHARS:
                    is_correct = True
            if not cleaned_text:
                continue
            current_option = {
                "text": cleaned_text,
                "is_correct": is_correct,
            }
        else:
            if current_option:
                line_indent = leading_ws_count(line)
                if line_has_marker(line_stripped):
                    cleaned_text, is_correct = clean_option_text(line_stripped)
                    if cleaned_text:
                        options.append(current_option)
                        current_option = {
                            "text": cleaned_text,
                            "is_correct": is_correct,
                        }
                        continue
                if line_indent > base_indent + 1:
                    current_option["text"] = normalize_space(
                        f"{current_option['text']} {line_stripped}"
                    )
                elif option_looks_complete(current_option["text"]):
                    cleaned_text, is_correct = clean_option_text(line_stripped)
                    if cleaned_text:
                        options.append(current_option)
                        current_option = {
                            "text": cleaned_text,
                            "is_correct": is_correct,
                        }
                else:
                    current_option["text"] = normalize_space(
                        f"{current_option['text']} {line_stripped}"
                    )
            else:
                line_indent = leading_ws_count(line)
                if question_lines and (
                    line_indent > base_indent + 1 or line_has_marker(line_stripped)
                ):
                    cleaned_text, is_correct = clean_option_text(line_stripped)
                    if cleaned_text:
                        current_option = {
                            "text": cleaned_text,
                            "is_correct": is_correct,
                        }
                        continue
                question_lines.append(line_stripped)

    if current_option:
        options.append(current_option)

    split_result = None
    if len(options) <= 1:
        split_result = split_bare_options(question_lines, len(options))

    if split_result is not None:
        question_lines, trailing_options = split_result
        promoted_options = [
            {"text": value, "is_correct": False} for value in trailing_options
        ]
        if options:
            options = promoted_options + options
        else:
            options = promoted_options

    if len(question_lines) > 1 and options:
        head = question_lines[0]
        tail_text = normalize_space(" ".join(question_lines[1:]))
        if (
            looks_like_definition_head(head)
            and tail_text
            and len(tail_text) > 40
            and not tail_text.endswith("?")
        ):
            cleaned_text, is_correct = clean_option_text(tail_text)
            if cleaned_text:
                options.insert(
                    0,
                    {
                        "text": cleaned_text,
                        "is_correct": is_correct,
                    },
                )
                question_lines = [head]

    question_text = normalize_space(" ".join(question_lines))

    return {
        "number": block.get("number"),
        "text": question_text,
        "options": options,
        "answer_hint": answer_hint,
    }


def parse_questions(text: str) -> List[Dict]:
    raw_lines = [
        line.replace("\u00a0", " ").rstrip()
        for line in text.replace("\r", "\n").split("\n")
    ]
    raw_lines = [line for line in raw_lines if line.strip()]
    raw_lines = expand_bullet_lines(raw_lines)
    blocks = split_into_question_blocks(raw_lines)

    if not blocks:
        return []

    questions = []
    for block in blocks:
        parsed = parse_question_block(block)
        if parsed["text"]:
            questions.append(parsed)

    return questions


def is_pdf_header_line(text: str) -> bool:
    stripped = text.strip()
    return (
        stripped.startswith("www.")
        or stripped.startswith("Bu f")
        or "Yekun imtahan" in stripped
        or stripped == "00830 Sosiologiya"
    )


def extract_pdf_line_groups(page, page_number: int) -> List[Dict]:
    words = page.extract_words(
        x_tolerance=2,
        y_tolerance=2,
        keep_blank_chars=False,
    )
    lines: List[Dict] = []

    for word in words:
        for line in lines:
            if abs(line["top"] - word["top"]) < 3:
                line["words"].append(word)
                line["top"] = min(line["top"], word["top"])
                line["bottom"] = max(line["bottom"], word["bottom"])
                break
        else:
            lines.append(
                {
                    "page": page_number,
                    "top": word["top"],
                    "bottom": word["bottom"],
                    "words": [word],
                }
            )

    grouped_lines: List[Dict] = []
    for line in lines:
        sorted_words = sorted(line["words"], key=lambda value: value["x0"])
        text = normalize_space(" ".join(word["text"] for word in sorted_words))
        if not text or is_pdf_header_line(text):
            continue
        grouped_lines.append(
            {
                "page": page_number,
                "top": line["top"],
                "bottom": line["bottom"],
                "x0": sorted_words[0]["x0"],
                "x1": sorted_words[-1]["x1"],
                "text": text,
            }
        )

    return sorted(grouped_lines, key=lambda line: line["top"])


def extract_pdf_radio_rows(page, page_number: int, lines: List[Dict]) -> List[Dict]:
    outer_circles = []
    selected_dots = []

    for curve in page.objects.get("curve", []):
        x0 = curve.get("x0", 0)
        width = curve.get("width", 0)
        height = curve.get("height", 0)

        if 25 <= x0 <= 40 and 4 <= width <= 6 and 4 <= height <= 6:
            outer_circles.append(curve)

        if (
            curve.get("non_stroking_color") == (0.0, 0.0, 0.0)
            and 25 <= x0 <= 40
            and 1 <= width <= 3
            and 1 <= height <= 3
        ):
            selected_dots.append(curve)

    centers: List[float] = []
    for circle in outer_circles:
        center_y = (circle["top"] + circle["bottom"]) / 2
        if not any(abs(center_y - existing) < 1.2 for existing in centers):
            centers.append(center_y)

    rows: List[Dict] = []
    for center_y in sorted(centers):
        candidates = [
            line
            for line in lines
            if 35 < line["x0"] < 90
            and line["top"] - 5 <= center_y <= line["bottom"] + 5
        ]
        if not candidates:
            continue

        line = min(
            candidates,
            key=lambda value: abs(((value["top"] + value["bottom"]) / 2) - center_y),
        )
        selected = any(
            abs(((dot["top"] + dot["bottom"]) / 2) - center_y) < 2.5
            for dot in selected_dots
        )
        rows.append(
            {
                "page": page_number,
                "center_y": center_y,
                "line": line,
                "selected": selected,
            }
        )

    return rows


def parse_radio_pdf_questions(file_bytes: bytes) -> List[Dict]:
    all_lines: List[Dict] = []
    all_radio_rows: List[Dict] = []

    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            lines = extract_pdf_line_groups(page, page_number)
            all_lines.extend(lines)
            all_radio_rows.extend(extract_pdf_radio_rows(page, page_number, lines))

    if not all_radio_rows:
        return []

    all_lines.sort(key=lambda line: (line["page"], line["top"], line["x0"]))
    all_radio_rows.sort(key=lambda row: (row["page"], row["center_y"]))

    question_starts: List[Dict] = []
    last_number: Optional[int] = None
    for line in all_lines:
        if line["x0"] > 40:
            continue
        match = match_question_line(line["text"], 0, last_number)
        if not match:
            continue
        number, rest = match
        question_starts.append({"line": line, "number": number, "rest": rest})
        last_number = number

    if not question_starts:
        return []

    questions: List[Dict] = []
    for index, start in enumerate(question_starts):
        end_page = (
            question_starts[index + 1]["line"]["page"]
            if index + 1 < len(question_starts)
            else 999999
        )
        end_top = (
            question_starts[index + 1]["line"]["top"]
            if index + 1 < len(question_starts)
            else 999999
        )

        def line_in_question(line: Dict) -> bool:
            if line["page"] < start["line"]["page"] or line["page"] > end_page:
                return False
            if line["page"] == start["line"]["page"] and line["top"] < start["line"]["top"] - 1:
                return False
            if line["page"] == end_page and line["top"] >= end_top - 1:
                return False
            return True

        def radio_in_question(row: Dict) -> bool:
            if row["page"] < start["line"]["page"] or row["page"] > end_page:
                return False
            if row["page"] == start["line"]["page"] and row["center_y"] < start["line"]["top"] - 1:
                return False
            if row["page"] == end_page and row["center_y"] >= end_top - 1:
                return False
            return True

        block_lines = [
            line
            for line in all_lines
            if line_in_question(line) and not is_page_marker_line(line["text"])
        ]
        radio_rows = [row for row in all_radio_rows if radio_in_question(row)]
        if not radio_rows:
            continue

        first_radio_line = radio_rows[0]["line"]
        question_lines = [
            dict(line)
            for line in block_lines
            if line["page"] < first_radio_line["page"]
            or (
                line["page"] == first_radio_line["page"]
                and line["top"] < first_radio_line["top"] - 1
            )
        ]
        if question_lines:
            question_lines[0]["text"] = start["rest"]

        options: List[Dict] = []
        for option_index, row in enumerate(radio_rows):
            next_row = (
                radio_rows[option_index + 1]
                if option_index + 1 < len(radio_rows)
                else None
            )
            option_lines = []
            for line in block_lines:
                if line["page"] < row["page"] or (
                    line["page"] == row["page"]
                    and line["top"] < row["line"]["top"] - 1
                ):
                    continue
                if next_row and (
                    line["page"] > next_row["page"]
                    or (
                        line["page"] == next_row["page"]
                        and line["top"] >= next_row["line"]["top"] - 1
                    )
                ):
                    continue
                if line["x0"] < 35:
                    continue
                option_lines.append(line)

            option_text = normalize_space(" ".join(line["text"] for line in option_lines))
            if option_text:
                options.append({"text": option_text, "is_correct": row["selected"]})

        question_text = normalize_space(" ".join(line["text"] for line in question_lines))
        if question_text and len(options) >= 2:
            questions.append(
                {
                    "number": start["number"],
                    "text": question_text,
                    "options": options,
                    "answer_hint": None,
                }
            )

    if len(questions) != len(question_starts):
        return []
    if len(questions) != sum(
        1 for question in questions if any(option["is_correct"] for option in question["options"])
    ):
        return []

    return questions


def parse_pdf_questions(file_bytes: bytes) -> List[Dict]:
    radio_questions = parse_radio_pdf_questions(file_bytes)
    if radio_questions:
        return radio_questions
    return parse_questions(extract_text_from_pdf_bytes(file_bytes))


def extract_text_from_pdf_bytes(file_bytes: bytes) -> str:
    text_parts: List[str] = []
    pages_lines: List[List[str]] = []
    header_counts: Dict[str, int] = {}
    footer_counts: Dict[str, int] = {}
    header_footer_lines = 3

    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text(x_tolerance=2, y_tolerance=2) or ""
            lines = [
                line.replace("\u00a0", " ").rstrip()
                for line in page_text.split("\n")
                if line.strip()
            ]
            pages_lines.append(lines)

            for line in lines[:header_footer_lines]:
                header_counts[line] = header_counts.get(line, 0) + 1
            for line in lines[-header_footer_lines:]:
                footer_counts[line] = footer_counts.get(line, 0) + 1

    header_remove = {line for line, count in header_counts.items() if count >= 2}
    footer_remove = {line for line, count in footer_counts.items() if count >= 2}

    for lines in pages_lines:
        cleaned: List[str] = []
        total = len(lines)
        for index, line in enumerate(lines):
            if index < header_footer_lines and line in header_remove:
                continue
            if index >= total - header_footer_lines and line in footer_remove:
                continue
            cleaned.append(line)
        text_parts.extend(cleaned)

    return "\n".join(text_parts)


def is_docx_bullet_paragraph(text: str, num_fmt: Optional[str]) -> bool:
    return num_fmt == "bullet" or bool(OPTION_BULLET_PATTERN.match(text))


def is_docx_numbered_paragraph(text: str, num_fmt: Optional[str]) -> bool:
    return num_fmt in DOCX_NUMBERED_FORMATS and not is_docx_bullet_paragraph(text, num_fmt)


def split_table_option_text(text: str, expected_parts: int) -> List[str]:
    cleaned = normalize_space(text)
    if not cleaned or expected_parts <= 1:
        return [cleaned] if cleaned else []

    sentence_parts = [
        normalize_space(part)
        for part in re.findall(r"[^.!?;]+[.!?;]?", cleaned)
        if normalize_space(part)
    ]
    if len(sentence_parts) >= expected_parts:
        return sentence_parts

    boundary_parts = [
        normalize_space(part)
        for part in re.split(r"(?<=[а-яa-z])\s+(?=[А-ЯA-Z«])", cleaned)
        if normalize_space(part)
    ]
    if len(boundary_parts) >= expected_parts:
        return boundary_parts

    return sentence_parts if sentence_parts else [cleaned]


def extract_docx_paragraphs(file_bytes: bytes) -> List[Dict]:
    with ZipFile(io.BytesIO(file_bytes)) as archive:
        document_root = ET.fromstring(archive.read("word/document.xml"))
        numbering_root = None
        if "word/numbering.xml" in archive.namelist():
            numbering_root = ET.fromstring(archive.read("word/numbering.xml"))

    num_map: Dict[str, str] = {}
    fmt_map: Dict[Tuple[str, str], Tuple[Optional[str], Optional[str]]] = {}
    override_starts: Dict[Tuple[str, str], int] = {}
    if numbering_root is not None:
        for num in numbering_root.findall("./w:num", DOCX_NS):
            num_id = num.get(f"{{{DOCX_NS['w']}}}numId")
            abstract = num.find("./w:abstractNumId", DOCX_NS)
            if num_id and abstract is not None:
                num_map[num_id] = abstract.get(f"{{{DOCX_NS['w']}}}val", "")
            for level_override in num.findall("./w:lvlOverride", DOCX_NS):
                ilvl = level_override.get(f"{{{DOCX_NS['w']}}}ilvl", "0")
                start_override = level_override.find("./w:startOverride", DOCX_NS)
                if num_id and start_override is not None:
                    override_starts[(num_id, ilvl)] = int(
                        start_override.get(f"{{{DOCX_NS['w']}}}val", "1")
                    )

        for abstract in numbering_root.findall("./w:abstractNum", DOCX_NS):
            abstract_id = abstract.get(f"{{{DOCX_NS['w']}}}abstractNumId")
            if abstract_id is None:
                continue
            for level in abstract.findall("./w:lvl", DOCX_NS):
                ilvl = level.get(f"{{{DOCX_NS['w']}}}ilvl", "0")
                num_fmt = level.find("./w:numFmt", DOCX_NS)
                lvl_text = level.find("./w:lvlText", DOCX_NS)
                start_value = level.find("./w:start", DOCX_NS)
                fmt_map[(abstract_id, ilvl)] = (
                    num_fmt.get(f"{{{DOCX_NS['w']}}}val") if num_fmt is not None else None,
                    lvl_text.get(f"{{{DOCX_NS['w']}}}val") if lvl_text is not None else None,
                    int(start_value.get(f"{{{DOCX_NS['w']}}}val", "1"))
                    if start_value is not None
                    else 1,
                )

    list_counters: Dict[Tuple[str, str], int] = {}
    
    def extract_paragraph_text(paragraph: ET.Element) -> str:
        text_parts = []
        for node in paragraph.iter():
            tag = node.tag.rsplit("}", 1)[-1]
            if tag == "t":
                text_parts.append(node.text or "")
            elif tag == "tab":
                text_parts.append("\t")
        return normalize_space(unescape("".join(text_parts)))

    def build_paragraph_record(paragraph: ET.Element) -> Optional[Dict]:
        text = extract_paragraph_text(paragraph)
        if not text:
            return None
        p_style = paragraph.find("./w:pPr/w:pStyle", DOCX_NS)
        num_pr = paragraph.find("./w:pPr/w:numPr", DOCX_NS)
        num_fmt = None
        lvl_text = None
        ilvl = "0"
        num_id = None
        abstract_id = None
        list_number = None
        if num_pr is not None:
            num_id_el = num_pr.find("./w:numId", DOCX_NS)
            ilvl_el = num_pr.find("./w:ilvl", DOCX_NS)
            num_id = num_id_el.get(f"{{{DOCX_NS['w']}}}val") if num_id_el is not None else None
            ilvl = ilvl_el.get(f"{{{DOCX_NS['w']}}}val", "0") if ilvl_el is not None else "0"
            abstract_id = num_map.get(num_id or "")
            if abstract_id is not None:
                num_fmt, lvl_text, start_value = fmt_map.get(
                    (abstract_id, ilvl), (None, None, 1)
                )
                if num_fmt == "decimal" and num_id is not None:
                    counter_key = (num_id, ilvl)
                    effective_start = override_starts.get(counter_key, start_value)
                    if counter_key not in list_counters:
                        list_counters[counter_key] = effective_start
                    else:
                        list_counters[counter_key] += 1
                    list_number = list_counters[counter_key]

        return {
            "text": text,
            "style": p_style.get(f"{{{DOCX_NS['w']}}}val") if p_style is not None else None,
            "num_fmt": num_fmt,
            "lvl_text": lvl_text,
            "level": ilvl,
            "num_id": num_id,
            "abstract_id": abstract_id,
            "list_number": list_number,
            "is_bullet": is_docx_bullet_paragraph(text, num_fmt),
            "is_numbered": is_docx_numbered_paragraph(text, num_fmt),
        }

    def make_synthetic_record(
        text: str,
        *,
        list_number: Optional[int] = None,
        is_bullet: bool = False,
        is_numbered: bool = False,
    ) -> Optional[Dict]:
        cleaned_text = normalize_space(text)
        if not cleaned_text:
            return None
        return {
            "text": cleaned_text,
            "style": "table",
            "num_fmt": "bullet" if is_bullet else ("decimal" if is_numbered else None),
            "lvl_text": "•" if is_bullet else ("%1." if is_numbered else None),
            "level": "1" if is_bullet else "0",
            "num_id": None,
            "abstract_id": None,
            "list_number": list_number,
            "is_bullet": is_bullet,
            "is_numbered": is_numbered,
        }

    def extract_table_records(table: ET.Element) -> List[Dict]:
        records: List[Dict] = []
        for row in table.findall("./w:tr", DOCX_NS):
            cell_texts: List[List[str]] = []
            for cell in row.findall("./w:tc", DOCX_NS):
                texts: List[str] = []
                for paragraph in cell.findall("./w:p", DOCX_NS):
                    text = extract_paragraph_text(paragraph)
                    if text:
                        texts.append(text)
                cell_texts.append(texts)

            if not any(cell_texts):
                continue

            question_number = None
            for texts in cell_texts:
                for value in texts:
                    match = re.match(r"^\s*(\d{1,4})[\.\)]\s*$", value)
                    if match:
                        question_number = int(match.group(1))
                        break
                if question_number is not None:
                    break

            if question_number is not None:
                question_text = ""
                for texts in reversed(cell_texts):
                    joined = normalize_space(" ".join(texts))
                    if joined and not re.match(r"^\d{1,4}[\.\)]$", joined):
                        question_text = joined
                        break
                record = make_synthetic_record(
                    f"{question_number}. {question_text}",
                    list_number=question_number,
                    is_numbered=True,
                )
                if record:
                    records.append(record)
                continue

            bullet_count = sum(
                1
                for texts in cell_texts
                for value in texts
                if value and set(value.replace(" ", "")) <= set(BULLET_CHARS)
            )
            option_source = next(
                (
                    [
                        value
                        for value in texts
                        if value and not set(value.replace(" ", "")) <= set(BULLET_CHARS)
                    ]
                    for texts in reversed(cell_texts)
                    if any(
                        value and not set(value.replace(" ", "")) <= set(BULLET_CHARS)
                        for value in texts
                    )
                ),
                [],
            )

            if bullet_count and option_source:
                joined_text = normalize_space(" ".join(option_source))
                option_texts = split_table_option_text(joined_text, bullet_count + 1)
                if len(option_texts) < bullet_count:
                    option_texts = option_source
                for idx, option_text in enumerate(option_texts):
                    record = make_synthetic_record(
                        option_text,
                        is_bullet=idx < bullet_count,
                    )
                    if record:
                        records.append(record)
                continue
            if bullet_count:
                continue

            for texts in cell_texts:
                for value in texts:
                    record = make_synthetic_record(value)
                    if record:
                        records.append(record)

        return records

    paragraphs: List[Dict] = []
    body = document_root.find(".//w:body", DOCX_NS)
    if body is None:
        return paragraphs

    for child in list(body):
        tag = child.tag.rsplit("}", 1)[-1]
        if tag == "p":
            record = build_paragraph_record(child)
            if record:
                paragraphs.append(record)
        elif tag == "tbl":
            paragraphs.extend(extract_table_records(child))

    return paragraphs


def parse_docx_questions(paragraphs: List[Dict]) -> List[Dict]:
    questions: List[Dict] = []
    current: Optional[Dict] = None
    last_number: Optional[int] = None
    continuation_words = {
        "в",
        "во",
        "и",
        "или",
        "по",
        "на",
        "с",
        "со",
        "к",
        "ко",
        "о",
        "об",
        "от",
        "до",
        "для",
        "при",
        "из",
        "под",
        "над",
        "за",
        "без",
    }

    def finalize_current() -> None:
        nonlocal current
        if not current:
            return

        question_text = normalize_space(" ".join(current["question_lines"]))
        options = [
            {
                "text": normalize_space(option["text"]),
                "is_correct": option["is_correct"],
            }
            for option in current["options"]
            if normalize_space(option["text"])
        ]

        if question_text and options:
            questions.append(
                {
                    "number": current["number"],
                    "text": question_text,
                    "options": options,
                    "answer_hint": None,
                }
            )
        current = None

    def next_non_empty(index: int) -> Optional[Dict]:
        for offset in range(index + 1, len(paragraphs)):
            candidate = paragraphs[offset]
            if candidate["text"]:
                return candidate
        return None

    def is_question_start(paragraph: Dict) -> bool:
        nonlocal current, last_number
        text = paragraph["text"]
        if paragraph["is_bullet"]:
            return False

        match = match_question_line(text, 0, last_number)
        if match:
            return True

        raw_text = text.lstrip()
        cleaned = strip_question_leading_noise(text)
        if raw_text.startswith("+"):
            return True

        if current and not current["options"]:
            return False

        if paragraph["is_numbered"] and cleaned and not cleaned.startswith("("):
            return True

        return False

    def start_question(paragraph: Dict) -> None:
        nonlocal current, last_number
        text = paragraph["text"]
        match = match_question_line(text, 0, last_number)
        question_number = None
        question_text = strip_question_leading_noise(text)

        if match:
            question_number, question_text = match
        elif paragraph.get("list_number") is not None:
            question_number = paragraph["list_number"]
        elif paragraph["is_numbered"]:
            question_number = (last_number + 1) if last_number is not None else None

        question_text = strip_question_leading_noise(question_text)
        current = {
            "number": question_number,
            "question_lines": [question_text] if question_text else [],
            "options": [],
        }
        if question_number is not None:
            last_number = question_number

    def looks_like_first_plain_option(index: int) -> bool:
        if current is None or current["options"]:
            return False
        if not current["question_lines"]:
            return False
        paragraph = paragraphs[index]
        text = paragraph["text"].strip()
        if paragraph["is_numbered"]:
            return False
        if text.startswith("(") and text.endswith(")"):
            return False
        next_item = next_non_empty(index)
        if next_item and next_item["is_bullet"]:
            return True
        question_text = normalize_space(" ".join(current["question_lines"]))
        lowered = question_text.lower()
        return question_text.endswith(":") or "выделите" in lowered

    def should_append_to_previous_option(previous_text: str, next_text: str) -> bool:
        cleaned_next, _ = clean_option_text(next_text)
        if not cleaned_next:
            return False
        if cleaned_next in {".", ",", ";", ":"}:
            return True
        previous_trimmed = previous_text.rstrip()
        if previous_trimmed.endswith((",", "(", "«", "-", "—")):
            return True
        last_word = previous_trimmed.split()[-1].strip(".,;:!?()\"«»").lower()
        if last_word in continuation_words:
            return True
        if (
            cleaned_next[0].islower()
            and len(previous_trimmed) >= 60
            and not previous_trimmed.endswith((".", ";", ":", "!", "?"))
        ):
            return True
        return False

    for index, paragraph in enumerate(paragraphs):
        text = paragraph["text"]
        if not text:
            continue

        if is_question_start(paragraph):
            finalize_current()
            start_question(paragraph)
            continue

        if current is None:
            continue

        bullet_like = paragraph["is_bullet"]

        if bullet_like or looks_like_first_plain_option(index) or current["options"]:
            cleaned_text, marker_correct = clean_option_text(text)
            if not cleaned_text:
                continue
            previous_option = current["options"][-1] if current["options"] else None
            if previous_option and should_append_to_previous_option(
                previous_option["text"], text
            ):
                previous_option["text"] = normalize_space(
                    f"{previous_option['text']} {cleaned_text}"
                )
                if bullet_like and not marker_correct:
                    previous_option["is_correct"] = False
                else:
                    previous_option["is_correct"] = (
                        previous_option["is_correct"] or marker_correct
                    )
                continue
            current["options"].append(
                {
                    "text": cleaned_text,
                    "is_correct": (not bullet_like) or marker_correct,
                }
            )
            continue

        if current["number"] is None and paragraph.get("list_number") is not None:
            current["number"] = paragraph["list_number"]
            last_number = paragraph["list_number"]

        current["question_lines"].append(strip_question_leading_noise(text))

    finalize_current()
    return questions


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
        file_bytes = file.read()
        questions = parse_uploaded_questions(filename, file_bytes)
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
            file_bytes = file.read()
            questions = parse_uploaded_questions(filename, file_bytes)
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
