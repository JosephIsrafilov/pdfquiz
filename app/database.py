import os
import sqlite3

try:
    import psycopg
    from psycopg.rows import dict_row
    from psycopg_pool import ConnectionPool
except ImportError:
    psycopg = None
    dict_row = None
    ConnectionPool = None

DATABASE_URL = os.environ.get("DATABASE_URL")
USING_POSTGRES = bool(DATABASE_URL)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.environ.get("DB_PATH", os.path.join(BASE_DIR, "app.db"))

_pool = None


def get_pool():
    global _pool
    if _pool is None and USING_POSTGRES:
        if ConnectionPool is None:
            raise RuntimeError("psycopg_pool required when DATABASE_URL is set")
        _pool = ConnectionPool(DATABASE_URL, kwargs={"row_factory": dict_row, "prepare_threshold": None}, min_size=1, max_size=10, open=True)
    return _pool


def get_db_connection():
    if USING_POSTGRES:
        pool = get_pool()
        return pool.connection()
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def db_query(query: str) -> str:
    if USING_POSTGRES:
        return query
    return query.replace("%s", "?")


def db_execute(connection, query: str, params=()):
    return connection.execute(db_query(query), params)


def get_first_column(row):
    if row is None:
        return None
    if isinstance(row, dict):
        return next(iter(row.values()))
    return row[0]


def init_db():
    db_dir = os.path.dirname(DB_PATH)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)

    with get_db_connection() as connection:
        if USING_POSTGRES:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    is_admin BOOLEAN NOT NULL DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """)
            connection.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    questions_json TEXT NOT NULL,
                    uploaded_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """)
            connection.execute("""
                CREATE TABLE IF NOT EXISTS results (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    document_id INTEGER REFERENCES documents(id) ON DELETE SET NULL,
                    source_label TEXT,
                    total_questions INTEGER,
                    quiz_size INTEGER,
                    graded INTEGER,
                    correct INTEGER,
                    unanswered INTEGER,
                    missing_answer_key INTEGER,
                    mistake_numbers_json TEXT,
                    attempt_json TEXT,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """)
            connection.execute("""
                CREATE TABLE IF NOT EXISTS courses (
                    id SERIAL PRIMARY KEY,
                    title_en TEXT NOT NULL,
                    title_ru TEXT NOT NULL,
                    is_active BOOLEAN NOT NULL DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """)
            connection.execute("""
                CREATE TABLE IF NOT EXISTS topics (
                    id SERIAL PRIMARY KEY,
                    course_id INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
                    title_en TEXT NOT NULL,
                    title_ru TEXT NOT NULL,
                    description_en TEXT,
                    description_ru TEXT,
                    sort_order INTEGER NOT NULL DEFAULT 0,
                    is_active BOOLEAN NOT NULL DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """)
            connection.execute("""
                CREATE TABLE IF NOT EXISTS questions (
                    id SERIAL PRIMARY KEY,
                    topic_id INTEGER NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
                    text_en TEXT,
                    text_ru TEXT,
                    options_json TEXT NOT NULL,
                    explanation_en TEXT,
                    explanation_ru TEXT,
                    difficulty TEXT NOT NULL DEFAULT 'beginner',
                    is_active BOOLEAN NOT NULL DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """)
            connection.execute("""
                CREATE TABLE IF NOT EXISTS quiz_sessions (
                    id SERIAL PRIMARY KEY,
                    token TEXT UNIQUE NOT NULL,
                    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
                    language TEXT NOT NULL,
                    question_order_json TEXT NOT NULL,
                    option_orders_json TEXT NOT NULL,
                    topic_ids_json TEXT NOT NULL,
                    completed BOOLEAN NOT NULL DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """)
            connection.execute("""
                CREATE TABLE IF NOT EXISTS groups (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    code TEXT UNIQUE NOT NULL,
                    created_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """)
            connection.execute("""
                CREATE TABLE IF NOT EXISTS group_members (
                    id SERIAL PRIMARY KEY,
                    group_id INTEGER NOT NULL REFERENCES groups(id) ON DELETE CASCADE,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    joined_at TIMESTAMP DEFAULT NOW(),
                    UNIQUE(group_id, user_id)
                )
            """)
            connection.execute("""
                CREATE TABLE IF NOT EXISTS rooms (
                    id SERIAL PRIMARY KEY,
                    code TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    created_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
                    topic_ids_json TEXT NOT NULL,
                    difficulty TEXT,
                    question_count INTEGER,
                    time_limit_minutes INTEGER,
                    max_attempts INTEGER,
                    is_active BOOLEAN NOT NULL DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT NOW(),
                    expires_at TIMESTAMP
                )
            """)
            connection.commit()
            alters = [
                "ALTER TABLE results ADD COLUMN IF NOT EXISTS attempt_json TEXT",
                "ALTER TABLE topics ADD COLUMN IF NOT EXISTS curriculum_key TEXT",
                "ALTER TABLE questions ADD COLUMN IF NOT EXISTS curriculum_key TEXT",
                "ALTER TABLE questions ADD COLUMN IF NOT EXISTS option_rationales_json TEXT",
                "ALTER TABLE questions ADD COLUMN IF NOT EXISTS question_type TEXT NOT NULL DEFAULT 'mcq'",
                "ALTER TABLE quiz_sessions ADD COLUMN IF NOT EXISTS room_id INTEGER REFERENCES rooms(id) ON DELETE CASCADE",
                "ALTER TABLE results ADD COLUMN IF NOT EXISTS room_id INTEGER REFERENCES rooms(id) ON DELETE CASCADE",
            ]
            for query in alters:
                try:
                    connection.execute(query)
                    connection.commit()
                except Exception:
                    connection.rollback()
        else:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    is_admin INTEGER NOT NULL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            connection.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    questions_json TEXT NOT NULL,
                    uploaded_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            connection.execute("""
                CREATE TABLE IF NOT EXISTS results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    document_id INTEGER REFERENCES documents(id) ON DELETE SET NULL,
                    source_label TEXT,
                    total_questions INTEGER,
                    quiz_size INTEGER,
                    graded INTEGER,
                    correct INTEGER,
                    unanswered INTEGER,
                    missing_answer_key INTEGER,
                    mistake_numbers_json TEXT,
                    attempt_json TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            connection.execute("""
                CREATE TABLE IF NOT EXISTS courses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title_en TEXT NOT NULL,
                    title_ru TEXT NOT NULL,
                    is_active INTEGER NOT NULL DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            connection.execute("""
                CREATE TABLE IF NOT EXISTS topics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    course_id INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
                    title_en TEXT NOT NULL,
                    title_ru TEXT NOT NULL,
                    description_en TEXT,
                    description_ru TEXT,
                    sort_order INTEGER NOT NULL DEFAULT 0,
                    is_active INTEGER NOT NULL DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            connection.execute("""
                CREATE TABLE IF NOT EXISTS questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic_id INTEGER NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
                    text_en TEXT,
                    text_ru TEXT,
                    options_json TEXT NOT NULL,
                    explanation_en TEXT,
                    explanation_ru TEXT,
                    difficulty TEXT NOT NULL DEFAULT 'beginner',
                    is_active INTEGER NOT NULL DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            connection.execute("""
                CREATE TABLE IF NOT EXISTS quiz_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    token TEXT UNIQUE NOT NULL,
                    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
                    language TEXT NOT NULL,
                    question_order_json TEXT NOT NULL,
                    option_orders_json TEXT NOT NULL,
                    topic_ids_json TEXT NOT NULL,
                    completed INTEGER NOT NULL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            connection.execute("""
                CREATE TABLE IF NOT EXISTS groups (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    code TEXT UNIQUE NOT NULL,
                    created_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            connection.execute("""
                CREATE TABLE IF NOT EXISTS group_members (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    group_id INTEGER NOT NULL REFERENCES groups(id) ON DELETE CASCADE,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(group_id, user_id)
                )
            """)
            connection.execute("""
                CREATE TABLE IF NOT EXISTS rooms (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    created_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
                    topic_ids_json TEXT NOT NULL,
                    difficulty TEXT,
                    question_count INTEGER,
                    time_limit_minutes INTEGER,
                    max_attempts INTEGER,
                    is_active INTEGER NOT NULL DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP
                )
            """)
            connection.commit()
            sqlite_alters = [
                "ALTER TABLE results ADD COLUMN attempt_json TEXT",
                "ALTER TABLE topics ADD COLUMN curriculum_key TEXT",
                "ALTER TABLE questions ADD COLUMN curriculum_key TEXT",
                "ALTER TABLE questions ADD COLUMN option_rationales_json TEXT",
                "ALTER TABLE questions ADD COLUMN question_type TEXT NOT NULL DEFAULT 'mcq'",
                "ALTER TABLE quiz_sessions ADD COLUMN room_id INTEGER REFERENCES rooms(id) ON DELETE CASCADE",
                "ALTER TABLE results ADD COLUMN room_id INTEGER REFERENCES rooms(id) ON DELETE CASCADE",
            ]
            for query in sqlite_alters:
                try:
                    connection.execute(query)
                    connection.commit()
                except Exception:
                    connection.rollback()
        connection.commit()
